from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pieces_per_carton = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Stock(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.PositiveIntegerField()
    quantity_unit = models.CharField(max_length=10, choices=(('pieces', 'Pieces'), ('cartons', 'Cartons')))

    def __str__(self):
        total_cartons, remaining_pieces = self.get_total_cartons_and_pieces()
        quantity_display = f"{total_cartons} cartons" if total_cartons > 0 else ""
        if remaining_pieces > 0:
            quantity_display += f" {remaining_pieces} pieces"
        return f"{self.store.name} - {self.product.name}: {self.quantity} {self.quantity_unit} ({quantity_display})"

    def get_total_cartons_and_pieces(self):
        if self.quantity_unit == 'cartons':
            total_pieces = self.quantity * self.product.pieces_per_carton
        else:
            total_pieces = self.quantity
        total_cartons = total_pieces // self.product.pieces_per_carton
        remaining_pieces = total_pieces % self.product.pieces_per_carton
        return total_cartons, remaining_pieces


class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    # code = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
