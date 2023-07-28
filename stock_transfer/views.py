from django.shortcuts import render, redirect
from inventory.models import Store, Product, Stock
from .models import StockTransfer, TransferItem
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def stock_transfer_view(request):
    if request.method == 'POST':
        # Get the selected stores and products from the request
        source_store_id = request.POST.get('source_store')
        destination_store_id = request.POST.get('destination_store')
        product_ids = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')
        units = request.POST.getlist('unit')

        # Validate if source and destination stores are different
        if source_store_id == destination_store_id:
            messages.error(request, "You entered the same source and destination stores, but they must be different for the transfer to happen, logically.")
            return redirect('stock_transfer:stock_transfer')

        # Create a stock transfer instance
        stock_transfer = StockTransfer.objects.create(
            transferred_by=request.user,
            source_store_id=source_store_id,
            destination_store_id=destination_store_id,
        )

        transfer_item_errors = []  # List to store transfer item error messages
        transfer_items = []  # List to store validated transfer items

        # Validate and create transfer items
        for product_id, quantity, unit in zip(product_ids, quantities, units):
            try:
                product = Product.objects.get(pk=product_id)
                quantity = int(quantity)

                # Get the available stock quantity
                stock = Stock.objects.get(store=source_store_id, product=product)
                available_quantity = stock.quantity

                # Check if the transfer quantity exceeds the available quantity
                if quantity > available_quantity:
                    transfer_item_errors.append(f"The quantity for product {product.name} exceeds the available stock in the source store.")
                else:
                    # Create a transfer item
                    transfer_item = TransferItem(
                        transfer=stock_transfer,
                        product=product,
                        quantity=quantity,
                        unit=unit
                    )
                    transfer_items.append(transfer_item)

            except (Product.DoesNotExist, ValueError, ValidationError):
                # Handle errors if the product doesn't exist or the quantity is invalid
                # You can display appropriate error messages or redirect to an error page
                pass

        if transfer_item_errors:
            # Pass the error messages and entered data back to the template
            stores = Store.objects.all()
            products = Product.objects.all()
            return render(request, 'stock_transfer/stock_transfer.html', {
                'stores': stores,
                'products': products,
                'transfer_item_errors': transfer_item_errors,
                'entered_data': {
                    'source_store': source_store_id,
                    'destination_store': destination_store_id,
                    'product_ids': product_ids,
                    'quantities': quantities,
                    'units': units,
                }
            })

        # Save the validated transfer items
        for transfer_item in transfer_items:
            transfer_item.save()

        messages.success(request, "Stock transfer complete.")
        return redirect('stock_transfer:stock_transfer')

    else:
        stores = Store.objects.all()
        products = Product.objects.all()
        return render(request, 'stock_transfer/stock_transfer.html', {'stores': stores, 'products': products})
