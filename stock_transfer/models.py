from django.db import models
from django.utils import timezone
from inventory.models import Store, Product, Stock
from accounts.models import User
from django.core.exceptions import ValidationError
from django.conf import settings


class StockTransfer(models.Model):
    source_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='source_transfers')
    destination_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='destination_transfers')
    transferred_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    transfer_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Transfer from {self.source_store} to {self.destination_store} by {self.transferred_by.username} at {self.transfer_time}"



class TransferItem(models.Model):
    transfer = models.ForeignKey(StockTransfer, on_delete=models.CASCADE, related_name='transfer_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=10, choices=(('pieces', 'Pieces'), ('cartons', 'Cartons')))
    

    def __str__(self):
        return f"{self.product} - {self.quantity} {self.unit}"

    def save(self, *args, **kwargs):
        # Validate if quantity exceeds available stock in the source store
        source_stock = Stock.objects.get(store=self.transfer.source_store, product=self.product)
        destination_stock, _ = Stock.objects.get_or_create(store=self.transfer.destination_store, product=self.product)

        if self.unit == 'cartons':
            # Convert cartons to pieces if the unit is 'pieces'
            self.quantity *= self.product.pieces_per_carton

        if self.quantity > source_stock.quantity:
            raise ValidationError("Transfer quantity exceeds the available stock in the source store.")

        # Subtract quantity from source store stock
        source_stock.quantity -= self.quantity
        source_stock.save()

        # Add quantity to destination store stock
        destination_stock, created = Stock.objects.get_or_create(store=self.transfer.destination_store, product=self.product)
        destination_stock.quantity += self.quantity
        destination_stock.save()

        super().save(*args, **kwargs)
