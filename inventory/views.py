from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Store, Stock, Customer
from .forms import ProductForm, CategoryForm, StoreForm, CustomerForm
# To display message
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required # only super admin can create the user


from accounts.models import User
from accounts.forms import UserRegistrationForm, UserUpdateForm

# Product
# Create
@staff_member_required(login_url='accounts:login')
def product_create(request):
    categories = Category.objects.all() # import the categories
    stores = Store.objects.all() # import the stores
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            # Success message
            messages.success(request, "A new product added...")
            return redirect('inventory:product_list')
    else:
        form = ProductForm()
    context = {
        'form': form,
        'categories': categories,
        'stores': stores
    }
    return render(request, 'admin/products/product_create.html', context)


# Read
@staff_member_required(login_url='accounts:login')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'admin/products/product_list.html', {'products': products})


@staff_member_required(login_url='accounts:login')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'admin/products/product_detail.html', {'product': product})


# Update
@staff_member_required(login_url='accounts:login')
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()  # Retrieve all categories
    stores = Store.objects.all()  # Retrieve all stores

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            # Success message
            messages.success(request, "Product updated...")
            return redirect('inventory:product_list')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'categories': categories,
        'stores': stores,
    }
    return render(request, 'admin/products/product_update.html', context)

# Delete
@staff_member_required(login_url='accounts:login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        # Success message
        messages.success(request, "Product deleted...")
        return redirect('inventory:product_list')
    return render(request, 'admin/products/product_delete.html', {'product': product})

# Store
@staff_member_required(login_url='accounts:login')
def store_create(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            # Success message
            messages.success(request, "A new store added...")
            return redirect('inventory:store_list')
    else:
        form = StoreForm()
    return render(request, 'admin/stores/store_create.html', {'form': form})

@staff_member_required(login_url='accounts:login')
def store_list(request):
    stores = Store.objects.all()
    return render(request, 'admin/stores/store_list.html', {'stores': stores})

@staff_member_required(login_url='accounts:login')
def store_detail(request, pk):
    store = get_object_or_404(Store, pk=pk)
    return render(request, 'admin/stores/store_detail.html', {'store': store})

@staff_member_required(login_url='accounts:login')
def store_update(request, pk):
    store = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            # Success message
            messages.success(request, "Store updated...")
            return redirect('inventory:store_list')
    else:
        form = StoreForm(instance=store)
    return render(request, 'admin/stores/store_update.html', {'form': form})

@staff_member_required(login_url='accounts:login')
def store_delete(request, pk):
    store = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        store.delete()
        # Success message
        messages.success(request, "Store deleted...")
        return redirect('inventory:store_list')
    return render(request, 'admin/stores/store_delete.html', {'store': store})

# Categories
@staff_member_required(login_url='accounts:login')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # Success message
            messages.success(request, "Category created...")
            return redirect('inventory:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'admin/categories/category_create.html', {'form': form})

@staff_member_required(login_url='accounts:login')
def category_list(request):
    categories = Category.objects.all()

    return render(request, 'admin/categories/category_list.html', {'categories': categories})

@staff_member_required(login_url='accounts:login')
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'admin/categories/category_detail.html', {'category': category})

@staff_member_required(login_url='accounts:login')
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            # Success message
            messages.success(request, "Category updated...")
            return redirect('inventory:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'admin/categories/category_update.html', {'form': form})

@staff_member_required(login_url='accounts:login')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        # Success message
        messages.success(request, "Category deleted...")
        return redirect('inventory:category_list')
    
    return render(request, 'admin/categories/category_delete.html', {'category': category})

# Staff
@staff_member_required(login_url='accounts:login')
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/users/user_list.html', {'users': users})


@staff_member_required(login_url='accounts:login')
def user_create(request):
    stores = Store.objects.all()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('inventory:user_list')
    else:
        
        form = UserRegistrationForm()
    context = {
        'stores': stores,
        'form': form
    }
    
    return render(request, 'admin/users/user_create.html', context)


@staff_member_required(login_url='accounts:login')
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'admin/users/user_detail.html', {'user': user})


@staff_member_required(login_url='accounts:login')
def user_update(request, pk):
    stores = Store.objects.all()
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('inventory:user_list')
    else:
        form = UserUpdateForm(instance=user)
    
    context = {
        'stores': stores,
        'form': form,
        'user': user,
    }
    
    return render(request, 'admin/users/user_update.html', context)

@staff_member_required(login_url='accounts:login')
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('inventory:user_list')
    
    return render(request, 'admin/users/user_delete.html', {'user': user})


# Stock
# Stock stores
@staff_member_required(login_url='accounts:login')
def store_stock(request):
    stores = Store.objects.all()
    context = {
        'stores': stores,
    }
    return render(request, 'admin/stock/store_stock.html', context)


# Create stock for a product in a store
@staff_member_required(login_url='accounts:login')
def stock_create(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    if request.method == 'POST':
        # Handle form submission and create the stock data
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        
        # Retrieve the product
        product = get_object_or_404(Product, id=product_id)
        
        # Create the stock object
        stock = Stock.objects.create(store=store, product=product, quantity=quantity)
        messages.success(request, "Stock created successfully.")
        return redirect('inventory:stock_list', id=store.id)

    # Retrieve all products to populate the product selection field
    products = Product.objects.all()

    context = {
        'store': store,
        'products': products,
    }
    return render(request, 'admin/stock/stock_create.html', context)


# Products in store
@staff_member_required(login_url='accounts:login')
def stock_list(request, id):
    store = get_object_or_404(Store, id=id)
    products = Product.objects.filter(stock__store=store).distinct()
    stock_data = []

    for product in products:
        stock = Stock.objects.get(store=store, product=product)
        total_cartons, remaining_pieces = stock.get_total_cartons_and_pieces()
        stock_data.append({
            'product': product,
            'quantity': stock.quantity,
            'total_cartons': total_cartons,
            'remaining_pieces': remaining_pieces
        })

    context = {
        'store': store,
        'stock_data': stock_data,
    }
    return render(request, 'admin/stock/stock_list.html', context)

# View the store product
@staff_member_required(login_url='accounts:login')
def stock_detail(request, store_id, product_id):
    store = get_object_or_404(Store, id=store_id)
    product = get_object_or_404(Product, id=product_id, stock__store=store)
    stock = Stock.objects.get(store=store, product=product)
    total_cartons, remaining_pieces = stock.get_total_cartons_and_pieces()

    context = {
        'store': store,
        'product': product,
        'stock': stock,
        'total_cartons': total_cartons,
        'remaining_pieces': remaining_pieces,
    }
    return render(request, 'admin/stock/stock_detail.html', context)

# Update the stock
@staff_member_required(login_url='accounts:login')
def stock_update(request, store_id, product_id):
    store = get_object_or_404(Store, id=store_id)
    product = get_object_or_404(Product, id=product_id)
    stock = Stock.objects.get(store=store, product=product)

    if request.method == 'POST':
        # Handle form submission and update the stock data
        quantity = request.POST.get('quantity')
        # Update the stock quantity with the submitted value
        stock.quantity = quantity
        stock.save()
        # Success message
        messages.success(request, "Product updated successfully.")
        return redirect('inventory:stock_detail', store_id, product_id)

    context = {
        'store': store,
        'product': product,
        'stock': stock,
    }
    return render(request, 'admin/stock/stock_update.html', context)

# Delete the stock
@staff_member_required(login_url='accounts:login')
def stock_delete(request, store_id, product_id):
    store = get_object_or_404(Store, id=store_id)
    product = get_object_or_404(Product, id=product_id)
    stock = Stock.objects.get(store=store, product=product)
    total_cartons, remaining_pieces = stock.get_total_cartons_and_pieces()

    if request.method == 'POST':
        # Delete the stock object
        stock.delete()
        messages.success(request, "Stock deleted successfully.")
        return redirect('inventory:stock_list', id=store.id)

    context = {
        'store': store,
        'product': product,
        'stock': stock,
        'total_cartons': total_cartons,
        'remaining_pieces': remaining_pieces,
    }
    return render(request, 'admin/stock/stock_delete.html', context)

# Customers
# Retrieve all customers
@login_required(login_url='accounts:login')
def customers_list(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers,
    }
    return render(request, 'inventory/customers.html', context)

# Create customer
@login_required(login_url='accounts:login')
def customers_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            # Success message
            messages.success(request, "Customer created...")
            return redirect('inventory:customers_list')
    else:
        form = CustomerForm()
    
    return render(request, 'inventory/customers_create.html', {'form': form})

# Read customers
@login_required(login_url='accounts:login')
def customers_detail(request, id):
    customer = get_object_or_404(Customer, id=id)
    context = {
        'customer': customer,
    }
    return render(request, 'inventory/customers_detail.html', context)

# Update customer
@login_required(login_url='accounts:login')
def customers_update(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            # Success message
            messages.success(request, "Customer updated successfully...")
            return redirect('inventory:customers_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'inventory/customers_update.html', {'form': form})

# Delete customer
@login_required(login_url='accounts:login')
def customers_delete(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, "Customer deleted successfully.")
        return redirect('inventory:customers_list')

    context = {
        'customer': customer,
        }
    return render(request, 'inventory/customers_delete.html', context)