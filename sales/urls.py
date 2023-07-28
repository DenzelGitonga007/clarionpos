from django.urls import path
from . import views


app_name = 'sales'

urlpatterns = [
    path('', views.sales_view, name="sales"),
    path('submit_sale/', views.submit_sale, name='submit_sale'),

    # Admin urls
    path('sales-list/', views.sales_list, name='sales_list'), # view sales list
    path('sale-delete/<int:pk>/', views.sales_delete, name='sales_delete'), # delete sale
    path('delete-selected-sales/', views.delete_selected_sales, name='delete_selected_sales'), # delete multiple sales

]