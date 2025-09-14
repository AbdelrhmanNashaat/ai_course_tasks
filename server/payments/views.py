import json
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PaymentTransaction, Child, Package, PackagePurchase


def _stripe_payment_method_types(method_key: str):
	# Map our 4 options to Stripe payment_method_types and options
	# Google Pay uses card via Payment Request API, so method type is 'card'
	mapping = {
		'card': ['card'],
		'google_pay': ['card'],
		'blik': ['blik'],
		'p24': ['p24'],
	}
	return mapping.get(method_key, ['card'])


class CreatePaymentIntentView(APIView):
	def post(self, request):
		stripe.api_key = settings.STRIPE_SECRET_KEY
		child_id = request.data.get('child_id')
		package_id = request.data.get('package_id')
		amount_cents = request.data.get('amount')
		currency = request.data.get('currency', 'usd')
		method_key = request.data.get('payment_method')  # card, google_pay, blik, p24

		if not all([child_id, package_id, amount_cents, method_key]):
			return Response({'detail': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			child = Child.objects.get(id=child_id)
			package = Package.objects.get(id=package_id, is_active=True)
		except (Child.DoesNotExist, Package.DoesNotExist):
			return Response({'detail': 'Invalid child or package'}, status=status.HTTP_404_NOT_FOUND)

		try:
			amount_cents = int(amount_cents)
		except (TypeError, ValueError):
			return Response({'detail': 'amount must be integer (smallest currency unit)'}, status=status.HTTP_400_BAD_REQUEST)

		payment_method_types = _stripe_payment_method_types(method_key)

		try:
			intent = stripe.PaymentIntent.create(
				amount=amount_cents,
				currency=currency,
				payment_method_types=payment_method_types,
				metadata={
					'child_id': str(child.id),
					'package_id': str(package.id),
					'payment_method': method_key,
				},
			)
		except stripe.error.StripeError as e:
			return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

		transaction = PaymentTransaction.objects.create(
			child=child,
			package=package,
			amount_cents=amount_cents,
			currency=currency,
			payment_method=method_key,
			stripe_payment_intent_id=intent['id'],
			status=intent['status'] if intent.get('status') else PaymentTransaction.Status.PENDING,
			client_secret=intent.get('client_secret', ''),
		)

		return Response({
			'client_secret': intent.get('client_secret'),
			'payment_intent_id': intent.get('id'),
			'status': intent.get('status'),
		})


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
	# Raw body is needed for signature verification. We bypass CSRF and parsers.
	parser_classes = []
	renderer_classes = []

	def post(self, request):
		stripe.api_key = settings.STRIPE_SECRET_KEY
		payload = request.body
		sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
		endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

		try:
			event = stripe.Webhook.construct_event(
				payload=payload, sig_header=sig_header, secret=endpoint_secret
			)
		except (ValueError, stripe.error.SignatureVerificationError):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		if event['type'] in ['payment_intent.succeeded', 'payment_intent.payment_failed', 'payment_intent.requires_action']:
			intent = event['data']['object']
			payment_intent_id = intent.get('id')
			status_value = intent.get('status', '')
			metadata = intent.get('metadata', {}) or {}
			try:
				transaction = PaymentTransaction.objects.select_related('child', 'package').get(
					stripe_payment_intent_id=payment_intent_id
				)
			except PaymentTransaction.DoesNotExist:
				return Response(status=status.HTTP_200_OK)

			# Update transaction status
			mapped_status = {
				'succeeded': PaymentTransaction.Status.SUCCEEDED,
				'requires_action': PaymentTransaction.Status.REQUIRES_ACTION,
				'processing': PaymentTransaction.Status.PENDING,
				'requires_payment_method': PaymentTransaction.Status.FAILED,
				'canceled': PaymentTransaction.Status.FAILED,
				'payment_failed': PaymentTransaction.Status.FAILED,
			}.get(status_value, PaymentTransaction.Status.PENDING)
			transaction.status = mapped_status
			transaction.client_secret = intent.get('client_secret', transaction.client_secret)
			transaction.save(update_fields=['status', 'client_secret', 'updated_at'])

			# On success, create the purchase record (idempotent)
			if mapped_status == PaymentTransaction.Status.SUCCEEDED:
				PackagePurchase.objects.get_or_create(
					transaction=transaction,
					defaults={
						'child_id': transaction.child_id,
						'package_id': transaction.package_id,
					}
				)

		return Response(status=status.HTTP_200_OK)

