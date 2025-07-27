from django.urls import path
from .views import (
    ProductListView, ProductCreateView,
    StockTransactionListView, StockTransactionCreateView,
    InventoryView
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/add/', ProductCreateView.as_view(), name='product-add'),
    path('transactions/', StockTransactionListView.as_view(), name='transaction-list'),
    path('transactions/add/', StockTransactionCreateView.as_view(), name='transaction-add'),
    path('inventory/', InventoryView.as_view(), name='inventory'),
] 