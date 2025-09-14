from django.contrib import admin
from .models import Child, Package, PaymentTransaction, PackagePurchase


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
	list_display = ("id", "first_name", "last_name", "parent")
	search_fields = ("first_name", "last_name", "parent__username")


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "price_cents", "currency", "is_active")
	list_filter = ("is_active", "currency")
	search_fields = ("name",)


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
	list_display = ("id", "stripe_payment_intent_id", "child", "package", "amount_cents", "currency", "payment_method", "status", "created_at")
	list_filter = ("status", "payment_method", "currency")
	search_fields = ("stripe_payment_intent_id", "child__first_name", "child__last_name")


@admin.register(PackagePurchase)
class PackagePurchaseAdmin(admin.ModelAdmin):
	list_display = ("id", "child", "package", "purchased_at")
	search_fields = ("child__first_name", "child__last_name", "package__name")
