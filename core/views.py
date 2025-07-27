from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Product, StockTransaction, StockDetail
from django import forms
from django.db.models import Sum, F, Q

# Forms
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'description']

class StockDetailForm(forms.ModelForm):
    class Meta:
        model = StockDetail
        fields = ['product', 'quantity']

StockDetailFormSet = forms.inlineformset_factory(
    StockTransaction, StockDetail, form=StockDetailForm, extra=1, can_delete=True
)

class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ['operation', 'reference']

# Views
class ProductListView(ListView):
    model = Product
    template_name = 'core/product_list.html'
    context_object_name = 'products'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'core/product_form.html'
    success_url = reverse_lazy('product-list')

class StockTransactionListView(ListView):
    model = StockTransaction
    template_name = 'core/transaction_list.html'
    context_object_name = 'transactions'
    ordering = ['-date']

class StockTransactionCreateView(View):
    def get(self, request):
        form = StockTransactionForm()
        formset = StockDetailFormSet()
        # Get current inventory for all products
        inventory = {}
        for product in Product.objects.all():
            inventory[product.id] = product.current_stock()
        return render(request, 'core/transaction_form.html', {'form': form, 'formset': formset, 'inventory': inventory})

    def post(self, request):
        form = StockTransactionForm(request.POST)
        formset = StockDetailFormSet(request.POST)
        # Get current inventory for all products (for redisplay on error)
        inventory = {}
        for product in Product.objects.all():
            inc_qty = StockDetail.objects.filter(
                product=product, transaction__operation='INCREASE'
            ).aggregate(total=Sum('quantity'))['total'] or 0
            dec_qty = StockDetail.objects.filter(
                product=product, transaction__operation='DECREASE'
            ).aggregate(total=Sum('quantity'))['total'] or 0
            inventory[product.id] = inc_qty - dec_qty
        if form.is_valid() and formset.is_valid():
            transaction = form.save()
            details = formset.save(commit=False)
            for detail in details:
                detail.transaction = transaction
                detail.save()
            return redirect('transaction-list')
        return render(request, 'core/transaction_form.html', {'form': form, 'formset': formset, 'inventory': inventory})

class InventoryView(View):
    def get(self, request):
        # Calculate inventory for each product
        products = Product.objects.all()
        inventory = []
        for product in products:
            inc_qty = StockDetail.objects.filter(
                product=product, transaction__operation='INCREASE'
            ).aggregate(total=Sum('quantity'))['total'] or 0
            dec_qty = StockDetail.objects.filter(
                product=product, transaction__operation='DECREASE'
            ).aggregate(total=Sum('quantity'))['total'] or 0
            inventory.append({
                'product': product,
                'quantity': inc_qty - dec_qty
            })
        return render(request, 'core/inventory.html', {'inventory': inventory})
