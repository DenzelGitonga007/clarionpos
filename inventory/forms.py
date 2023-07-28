from django import forms
from .models import Product, Category, Store, Customer


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'

# Customer form
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
