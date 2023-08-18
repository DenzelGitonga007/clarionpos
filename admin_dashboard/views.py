from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import User
from inventory.models import *
from django.http import JsonResponse
from sales.models import Sale, SaleItem, Expense, Debtor
# For authentication
from django.contrib.auth.decorators import login_required # only super admin can create the user-- has to log in
from django.contrib.admin.views.decorators import staff_member_required # only super admin can create the user
import json
from django.db.models import Case, When, Sum, Value, F, DecimalField
from datetime import datetime
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.contrib import messages

import datetime


# Render the main content
@staff_member_required(login_url='accounts:login')
def admin_dashboard(request):
    today = timezone.now().date()

    # Calculate total sales for today
    start_of_day = timezone.datetime(today.year, today.month, today.day, 0, 0, 0, tzinfo=timezone.utc)
    end_of_day = start_of_day + timezone.timedelta(days=1)
    
    # Calculate total sales
    total_sales_today = Sale.objects.filter(date__gte=start_of_day, date__lt=end_of_day).aggregate(total_sales=Sum('total_amount'))['total_sales']

    # Calculate total expenses for today
    total_expenses_today = Expense.objects.filter(date__gte=start_of_day, date__lt=end_of_day).aggregate(total_expenses=Sum('amount'))['total_expenses']

    # Total products
    total_products = Product.objects.count()
    # Count the number of customers in the system
    total_customers = Customer.objects.count()

    # Retrieve the debts
    total_debts = Debtor.objects.aggregate(total_debts=Sum('outstanding_balance'))['total_debts']


    context = {
        'today': today,
        'total_products': total_products,
        'total_sales_today': total_sales_today,
        'total_expenses_today': total_expenses_today,
        'total_customers': total_customers,
        'total_debts': total_debts,
        }
    return render(request, 'home/index.html', context)

# Select the sale store
@staff_member_required(login_url='accounts:login')
def select_expense_store(request):
    # Retrieve the stores
    stores = Store.objects.all()
    context = {
        'stores': stores,
    }
    # Present to the page
    return render(request, 'admin/sales/select_expense_store.html', context)
# End of select sale store 

    
# Sales
# Select the sale store
@staff_member_required(login_url='accounts:login')
def select_sale_store(request):
    # Retrieve the stores
    stores = Store.objects.all()
    context = {
        'stores': stores,
    }
    # Present to the page
    return render(request, 'admin/sales/select_store.html', context)
# End of select sale store 


# Sales for the selected store
@staff_member_required(login_url='accounts:login')
def sales_list(request, id):
    # Get today's date
    today = timezone.now().date()

    # Calculate start and end of current day
    start_of_day = timezone.datetime(today.year, today.month, today.day, 0, 0, 0, tzinfo=timezone.utc)
    end_of_day = start_of_day + timezone.timedelta(days=1)

    store = get_object_or_404(Store, id=id)  # Retrieve the store based on the provided ID

    # Retrieve the selected start_date and end_date from the query parameters
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    sales = Sale.objects.filter(sold_by__store=store)

    if start_date_str and end_date_str:
        # Parse start_date and end_date if provided
        start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timezone.timedelta(days=1)

        # Filter sales for the store within the selected date range
        sales = Sale.objects.filter(sold_by__store=store, date__gte=start_date, date__lt=end_date)

        # Obtain total sales for the filtered sales
        total_sale = sales.aggregate(total_amount=Sum('total_amount'))['total_amount']
    else:
        # Filter sales for the store and the current day
        sales = Sale.objects.filter(sold_by__store=store, date__gte=start_of_day, date__lt=end_of_day)
        
        # Obtain total sales for the store
        total_sale = sales.aggregate(total_amount=Sum('total_amount'))['total_amount']

    # Calculate total amounts for each payment method
    cash_total = sales.filter(payment_method__name='CASH').aggregate(cash_total=Sum('total_amount'))['cash_total'] or 0
    till_total = sales.filter(payment_method__name='TILL').aggregate(till_total=Sum('total_amount'))['till_total'] or 0
    bank_total = sales.filter(payment_method__name='BANK').aggregate(bank_total=Sum('total_amount'))['bank_total'] or 0

    # Retrieve expenses for the store based on selected dates
    if start_date_str and end_date_str:
        expenses = Expense.objects.filter(store=store, date__gte=start_date, date__lt=end_date)
    else:
        expenses = Expense.objects.filter(store=store, date__gte=start_of_day, date__lt=end_of_day)
    
    total_expenses = expenses.aggregate(total_amount=Sum('amount'))['total_amount'] or 0


    context = {
        'today': today,
        'store': store,
        'sales': sales,
        'total_sale': total_sale,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'cash_total': cash_total,
        'till_total': till_total,
        'bank_total': bank_total,
        'total_expenses' : total_expenses,
    }
    return render(request, 'admin/sales/sales_list.html', context)





# Original sales_list view Add all the sales since start of sell
# def sales_list(request, id):
#     # Get today's date
#     today = timezone.now().date()

#     store = get_object_or_404(Store, id=id)  # Retrieve the store based on the provided ID
#     sales = Sale.objects.filter(sold_by__store=store)
#     # Obtain total sales
#     total_sale = sales.aggregate(total_amount=Sum('total_amount'))['total_amount']
#     context = {
#         'today': today,
#         'store': store,
#         'sales': sales,
#         'total_sale': total_sale,
#     }
#     return render(request, 'admin/sales/sales_list.html', context)
# End of sales for the selected store

# View the sale detail
@staff_member_required(login_url='accounts:login')
def sale_detail(request, store_id, sale_id):
    store = get_object_or_404(Store, id=store_id)
    sales = get_object_or_404(Sale, id=sale_id, sold_by__store=store)
    
    context = {
        'store' : store,
        'sales': sales,
    }
    return render(request, 'admin/sales/sales_detail.html', context)
# End of sale detail

# Update sale
@staff_member_required(login_url='accounts:login')
def sale_update(request, store_id, sale_id):
    store = get_object_or_404(Store, id=store_id)
    sale = get_object_or_404(Sale, id=sale_id, sold_by__store=store)
    customers = Customer.objects.all()
    if request.method == 'POST':
        # Update the sale object with the submitted data
        customer_id = request.POST.get('customer')
        sale.customer = get_object_or_404(Customer, id=customer_id)
        sale.total_amount = request.POST.get('total_amount')
        sale.rendered_amount = request.POST.get('rendered_amount')
        sale.balance = request.POST.get('balance')

        # Save the updated sale object
        sale.save()
        # Success message
        messages.success(request, "Sale updated successfully.")
        return redirect('admin_dashboard:sale_detail', store_id=store_id, sale_id=sale_id)
    
    context = {
        'customers': customers,
        'store': store,
        'sale': sale,
    }
    return render(request, 'admin/sales/sales_update.html', context)
# End of Update sale

# Delete sale
@staff_member_required(login_url='accounts:login')
def sale_delete(request, store_id, sale_id):
    store = get_object_or_404(Store, id=store_id)
    sale = get_object_or_404(Sale, id=sale_id, sold_by__store=store)

    if request.method == 'POST':
        sale.delete()
        messages.success(request, "Stock deleted successfully.")
        return redirect('admin_dashboard:sales_list', id=store_id)

    context = {
        'store': store,
        'sale': sale,
    }
    return render(request, 'admin/sales/sales_delete.html', context)

# End of delete sale










# Original admin dashboard
# @staff_member_required(login_url='accounts:login')
# def admin_dashboard(request):
#     # Retrieve the sales items and aggregate the quantities sold for each product
#     sales_items = SaleItem.objects.select_related('product').values('product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')

#     product_labels = [item['product__name'] for item in sales_items]
#     product_quantities = [float(item['total_quantity']) for item in sales_items]
    

#     # Retrieve the sales data for the chart
#     sales = Sale.objects.annotate(sale_date=TruncDate('date')).values('sale_date').annotate(total_sales=Sum('total_amount')).order_by('sale_date')

#     # labels = [sale['sale_date'].strftime('%Y-%m-%d') for sale in sales]
#     # data = [float(sale['total_sales']) for sale in sales]
#     labels = []
#     data = []

#     for sale in sales:
#         sale_date = sale.get('sale_date')
#         if sale_date:
#             labels.append(sale_date.strftime('%Y-%m-%d'))
#             data.append(float(sale['total_sales']))
#         else:
#             # Handle cases where sale_date is None, e.g., by skipping or providing a default value
#             pass

    

#     sales_data = {
#         'labels': labels,
#         'datasets': [
#             {
#                 'label': 'Sales',
#                 'data': data,
#                 'backgroundColor': 'rgba(54, 162, 235, 0.5)',
#                 'borderColor': 'rgba(54, 162, 235, 1)',
#                 'borderWidth': 1
#             }
#         ]
#     }

#     sales_data_json = json.dumps(sales_data)

#     context = {
#         'sales_data': sales_data_json,
#         'product_labels': product_labels, 
#         'product_quantities': product_quantities,
#     }

#     return render(request, 'admin/dashboard.html', context)
