from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Product URLs
    path('product/create/', views.product_create, name='product_create'),
    path('product/list/', views.product_list, name='product_list'),
    path('product/detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/update/<int:pk>/', views.product_update, name='product_update'),
    path('product/delete/<int:pk>/', views.product_delete, name='product_delete'),

    # Category URLs
    path('category/create/', views.category_create, name='category_create'),
    path('category/list/', views.category_list, name='category_list'),
    path('category/detail/<int:pk>/', views.category_detail, name='category_detail'),
    path('category/update/<int:pk>/', views.category_update, name='category_update'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),

    # Store URLs
    path('store/create/', views.store_create, name='store_create'),
    path('store/list/', views.store_list, name='store_list'),
    path('store/detail/<int:pk>/', views.store_detail, name='store_detail'),
    path('store/update/<int:pk>/', views.store_update, name='store_update'),
    path('store/delete/<int:pk>/', views.store_delete, name='store_delete'),


    # Users URLs
    path('users/', views.user_list, name='user_list'), # view users
    path('create/', views.user_create, name='user_create'),
    path('detail/<int:pk>/', views.user_detail, name='user_detail'),
    path('update/<int:pk>/', views.user_update, name='user_update'),
    path('delete/<int:pk>/', views.user_delete, name='user_delete'),

    # Stocks URLs
    path('store-stock/', views.store_stock, name='store_stock'), # display the stores
    path('stock/create/<int:store_id>/', views.stock_create, name='stock_create'), # create stock
    path('stock/list/<int:id>/', views.stock_list, name='stock_list'), # view products in the selected store
    path('stock/detail/<int:store_id>/<int:product_id>/', views.stock_detail, name='stock_detail'), # view the store product details
    path('stock-store-product/update/<int:store_id>/<int:product_id>/', views.stock_update, name='stock_update'), # update the selected product in the store
    path('stock-store-product/delete/<int:store_id>/<int:product_id>/', views.stock_delete, name='stock_delete'), # delete product

    # Customers
    path('customers/', views.customers_list, name="customers_list"), # retrieve customers list
    path('customer/create/', views.customers_create, name='customers_create'), # create customer
    path('customer/<int:id>/detail/', views.customers_detail, name='customers_detail'), # read customers detail
    path('customer/<int:id>/update/', views.customers_update, name='customers_update'), # update customer
    path('customer/<int:id>/delete/', views.customers_delete, name='customers_delete'), # delete customer

    # Debtors
    path('debtors/', views.debtors_list, name="debtors_list"), # retrieve the debtors
]
