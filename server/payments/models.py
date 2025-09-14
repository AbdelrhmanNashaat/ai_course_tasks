from django.db import models
from django.contrib.auth.models import User


class Child(models.Model):
	parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	birth_date = models.DateField(null=True, blank=True)

	def __str__(self) -> str:
		return f"{self.first_name} {self.last_name}"


class Package(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	price_cents = models.PositiveIntegerField(help_text='Price in the smallest currency unit')
	currency = models.CharField(max_length=10, default='usd')
	is_active = models.BooleanField(default=True)

	def __str__(self) -> str:
		return self.name


class PaymentTransaction(models.Model):
	class PaymentMethod(models.TextChoices):
		CARD = 'card', 'Card'
		GOOGLE_PAY = 'google_pay', 'Google Pay'
		BLIK = 'blik', 'BLIK'
		P24 = 'p24', 'Przelewy24'

	class Status(models.TextChoices):
		REQUIRES_ACTION = 'requires_action', 'Requires Action'
		PENDING = 'pending', 'Pending'
		SUCCEEDED = 'succeeded', 'Succeeded'
		FAILED = 'failed', 'Failed'

	child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='payments')
	package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name='payments')
	amount_cents = models.PositiveIntegerField()
	currency = models.CharField(max_length=10, default='usd')
	payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
	stripe_payment_intent_id = models.CharField(max_length=255, unique=True)
	status = models.CharField(max_length=32, choices=Status.choices, default=Status.PENDING)
	client_secret = models.CharField(max_length=255, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return f"{self.stripe_payment_intent_id} - {self.status}"


class PackagePurchase(models.Model):
	child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='purchases')
	package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name='purchases')
	transaction = models.OneToOneField(PaymentTransaction, on_delete=models.CASCADE, related_name='purchase')
	purchased_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Purchase {self.id} - {self.child} - {self.package}"
