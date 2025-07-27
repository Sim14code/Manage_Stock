from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import StockDetail
from django.db import transaction as db_transaction


@receiver(post_save, sender=StockDetail)
def update_stock_and_alert(sender, instance, **kwargs):
    @db_transaction.on_commit
    def notify_or_validate():
        stock = instance.product.current_stock()
        if stock <= 0:
            print(f"⚠️ ALERT: Product '{instance.product.name}' is out of stock or negative (Current: {stock})")
    notify_or_validate()


@receiver(pre_save, sender=StockDetail)
def prevent_negative_stock(sender, instance, **kwargs):
    if instance.transaction.operation == "DECREASE":
        current_stock = instance.product.current_stock()

        # If editing, rollback old quantity
        if instance.pk:
            old = StockDetail.objects.get(pk=instance.pk)
            current_stock += old.quantity

        if current_stock < instance.quantity:
            raise ValidationError(
                f"❌ Insufficient stock for '{instance.product.name}'. "
                f"Available: {current_stock}, Tried to remove: {instance.quantity}"
            )
