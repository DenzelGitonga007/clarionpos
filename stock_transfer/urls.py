from django.urls import path
from . import views

app_name = 'stock_transfer'

urlpatterns = [
    path('stock_transfer/', views.stock_transfer_view, name='stock_transfer'),
]

