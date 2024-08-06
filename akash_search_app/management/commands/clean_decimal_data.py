from django.core.management.base import BaseCommand
from decimal import Decimal, InvalidOperation
from akash_search_app.models import Product

class Command(BaseCommand):
    help = 'Clean invalid decimal data from Product model'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        for product in products:
            try:
                # Validate MRP and SellPrice
                product.MRP = Decimal(str(product.MRP).strip())
                product.SellPrice = Decimal(str(product.SellPrice).strip())
                product.save()
            except (ValueError, InvalidOperation):
                # If conversion fails, set fields to None or default values
                product.MRP = None
                product.SellPrice = None
                product.save()

        self.stdout.write(self.style.SUCCESS('Successfully cleaned up decimal data'))
