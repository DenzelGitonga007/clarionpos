from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Sale, SaleItem, Expense,Debtor
from inventory.models import Product, Customer, PaymentMethod, Stock
import json
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required # only super admin can create the user
from django.utils import timezone
from django.contrib import messages
from django.db.models import DateField, Sum
from django.views.decorators.http import require_GET
from decimal import Decimal


# Expenses
# Enter Expenses
@login_required(login_url='accounts:login')
def expense(request):
    if request.method == 'POST':
        date = request.POST.get('date')  # Get the date once
        descriptions = request.POST.getlist('description[]')
        amounts = request.POST.getlist('amount[]')
        print("Date:", date)
        print("Description: ", descriptions)
        print("Amounts: ", amounts)
        for description, amount in zip(descriptions, amounts):
            expense = Expense(
                recorded_by=request.user,
                store=request.user.store,
                date=date,  # Use the same date for all expenses
                description=description,
                amount=amount
            )
            expense.save()

        # Success message
        messages.success(request, "Expenses saved successfully")
        return redirect('accounts:home')

    context = {}
    return render(request, 'sales/expenses.html', context)

# End of expense entry

# Make sale
@login_required(login_url='accounts:login')
@csrf_exempt
def submit_sale(request):
    if request.method == 'POST':
        try:
            # Parse the JSON string to a Python object
            sale_data = json.loads(request.body)
            # Retrieve the sale items from the sale data
            sale_items = sale_data['saleItems']
            # Create a new sale object
            sale = Sale.objects.create(
                sold_by=request.user,
                total_amount=0,  # Initialize total amount
                rendered_amount=sale_data['renderedAmount'],
                balance=sale_data['balance'],
                customer_id=sale_data['customerId'],
                payment_method_id=sale_data['payment_methodId'],
            )

            # Calculate the total amount for the sale
            total_amount = 0

            # Iterate over the sale items received from the request
            for item in sale_items:
                product_name = item['productName']
                quantity = item['quantity']
                unit = item['unit']
                total = item['total']

                # Create a sale item object and associate it with the sale
                sale_item = SaleItem(
                    sale=sale,
                    product=Product.objects.get(name=product_name),
                    quantity=quantity,
                    unit=unit,
                    sale_price=total
                )

                sale_item.save()

                # Update the total amount for the sale
                total_amount += total

                # Convert quantity to pieces if the unit is 'Cartons'
                if unit == 'Cartons':
                    quantity *= sale_item.product.pieces_per_carton

                # Subtract the sold quantity from the stock
                stock = get_object_or_404(Stock, store=request.user.store, product=sale_item.product)
                stock.quantity -= quantity
                stock.save()

            # Update the total amount for the sale
            sale.total_amount = total_amount

            # Calculate the balance
            rendered_amount = sale_data['renderedAmount']
            rendered_amount = sale_data['renderedAmount']
            balance = Decimal(rendered_amount - total_amount)
            sale.balance = balance

            # # Check if the customer has become a debtor
            # if balance < 0 and not Debtor.objects.filter(customer=sale.customer).exists():
            #     Debtor.objects.create(customer=sale.customer, outstanding_balance=balance)

            # Check if the customer has become a debtor
            debtor = Debtor.objects.filter(customer=sale.customer).first()
            if debtor:
                debtor.outstanding_balance += balance
                debtor.save()
            else:
                if balance < 0:
                    Debtor.objects.create(customer=sale.customer, outstanding_balance=balance)

            
            # Save the sale
            sale.save()

            # Sale successfully created
            return JsonResponse({'message': 'Sale submitted successfully.'})

        except Exception as e:
            print("Exception: ",e)
            # Failed to create the sale
            return JsonResponse({'error': str(e)}, status=400)
            print("Exception: ",e)
        print("Exception: ",e)

    # Invalid request method
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

# End of sale

# Present the sale page
@login_required(login_url='accounts:login')
def sales_view(request):
    products = Product.objects.all()
    customers = Customer.objects.all()
    payment_methods = PaymentMethod.objects.all()
    units = SaleItem._meta.get_field('unit').choices
    product_json = []
    context = {
        'page_title': "Point of Sale",
        'products': products,
        'customers': customers,
        'payment_methods': payment_methods,
        'units': units,
        'product_json': json.dumps(product_json)
    }
    return render(request, 'sales/sales.html', context)
# End of sale page

# Filter the sales
@staff_member_required(login_url='accounts:login')
@require_GET
def sales_list(request):    
    sales = Sale.objects.order_by('-date')

    # Obtain total sales
    total_sale = sales.aggregate(total_amount=Sum('total_amount'))['total_amount']
    # Apply date filters
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    if from_date and to_date:
        sales = sales.filter(date__range=[from_date, to_date])

    context = {
        'sales': sales,
        'request': request,  # Pass the request object to template for accessing query parameters
        'total_sale': total_sale,
    }
    return render(request, 'admin/sales/general_sales_list.html', context)
# End of filter sales

# Delete product
@staff_member_required(login_url='accounts:login')
def sales_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        # Success message
        messages.success(request, "Sale deleted successfully...")
        return redirect('sales:sales_list')
    return render(request, 'admin/sales/sales_delete.html', {'sale': sale})
# End of delete product


# Delete selected sales
@staff_member_required(login_url='accounts:login')
def delete_selected_sales(request):
    if request.method == 'POST' and 'selected_sales[]' in request.POST:
        selected_sales = request.POST.getlist('selected_sales[]')
        Sale.objects.filter(pk__in=selected_sales).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
# End of delete selected sales

# Sales for admin

# End of sales for admin
