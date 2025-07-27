from django.contrib import admin
from .models import Product, StockTransaction, StockDetail

admin.site.register(Product)
admin.site.register(StockTransaction)
admin.site.register(StockDetail)
