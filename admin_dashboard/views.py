from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import User
from inventory.models import *
from django.http import JsonResponse
from sales.models import Sale, SaleItem
# For authentication
from django.contrib.auth.decorators import login_required # only super admin can create the user-- has to log in
from django.contrib.admin.views.decorators import staff_member_required # only super admin can create the user
import json
from django.db.models import Sum, F
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.contrib import messages


# The main content
@staff_member_required(login_url='accounts:login')
def admin_dashboard(request):
    today = timezone.now().date()  # Get the current date
    # Retrieve the total sales for the current day
    total_sales_today = Sale.objects.filter(date__date=today).aggregate(total=Sum('total_amount'))['total']
    # Count the number of customers in the system
    total_customers = Customer.objects.count()
    # Count the number of products in the system
    total_products = Product.objects.count()
    context = {
        'today': today,
        'total_sales_today': total_sales_today,
        'total_customers': total_customers,
        'total_products': total_products
    }
    return render(request, 'home/index.html', context)

    
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
    store = get_object_or_404(Store, id=id)  # Retrieve the store based on the provided ID
    sales = Sale.objects.filter(sold_by__store=store)
    # Obtain total sales
    total_sale = sales.aggregate(total_amount=Sum('total_amount'))['total_amount']
    context = {
        'store': store,
        'sales': sales,
        'total_sale': total_sale,
    }
    return render(request, 'admin/sales/sales_list.html', context)
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
