from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'), # dashboard
    
    # Sales
    path('select-store/', views.select_sale_store, name='select_sale_store'), # select the store for the sale
    path('sales/<int:id>/', views.sales_list, name='sales_list'), # view sales in the selected store
    path('sale/detail/<int:store_id>/<int:sale_id>/', views.sale_detail, name="sale_detail"), # view sale detail
    path('sale/update/<int:store_id>/<int:sale_id>/', views.sale_update, name='sale_update'), # update sale
    path('sale/delete/<int:store_id>/<int:sale_id>/', views.sale_delete, name='sale_delete'), # delete sale

    # Expenses
    path('select-expense-store/', views.select_expense_store, name='select_expense_store'), # select the store for the expense


]


