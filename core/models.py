from django.db import models
from django.db.models import Sum, F, Case, When, IntegerField
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction as db_transaction
from django.core.exceptions import ValidationError


class Product(models.Model):  # prodmast
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def current_stock(self):
        stock = self.stockdetail_set.annotate(
            sign=Case(
                When(transaction__operation="INCREASE", then=1),
                When(transaction__operation="DECREASE", then=-1),
                output_field=IntegerField()
            )
        ).aggregate(
            total=Sum(F('quantity') * F('sign'))
        )['total'] or 0
        return stock

    def __str__(self):
        return f"{self.name} ({self.sku})"


class StockTransaction(models.Model):
    OPERATION_CHOICES = [
        ("INCREASE", "Increase (Stock In)"),
        ("DECREASE", "Decrease (Stock Out)")
    ]
    date = models.DateTimeField(auto_now_add=True)
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES, default="INCREASE")
    reference = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.get_operation_display()} #{self.id} on {self.date.strftime('%Y-%m-%d')}"


class StockDetail(models.Model):  # stckdetail
    transaction = models.ForeignKey(StockTransaction, on_delete=models.CASCADE, related_name="details")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.product} x {self.quantity} ({self.transaction})"

    class Meta:
        unique_together = ("transaction", "product")
