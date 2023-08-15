from django.core.exceptions import ValidationError
from django.db import models
from inventory.models import Product, Customer, PaymentMethod, Stock, Store
from django.contrib.auth.models import User
from django.conf import settings


class Sale(models.Model):
    sold_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    rendered_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.sold_by, self.date, self.total_amount, self.rendered_amount, self.balance, self.customer)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=(('pieces', 'Pieces'), ('cartons', 'Cartons')))  # Field to store the unit of the product
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.unit == 'cartons':
            # Convert cartons to pieces if the unit is 'pieces'
            self.quantity *= self.product.pieces_per_carton

        if self.sale_price < self.product.price:
            raise ValidationError("Sale price cannot be below the product's price.")
        self.sale_price = self.product.price * self.quantity  # Calculate the sale_price
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} {} {} {} {}".format(self.sale, self.product, self.unit, self.quantity, self.sale_price)
