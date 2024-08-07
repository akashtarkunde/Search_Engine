from djongo import models
from decimal import Decimal

class Product(models.Model):
    _id = models.ObjectIdField(db_column='_id')
    BrandName = models.CharField(max_length=255, db_column='BrandName')
    ProductID = models.CharField(max_length=255, db_column='ProductID')
    ProductName = models.CharField(max_length=255, db_column='ProductName')
    BrandDesc = models.TextField(db_column='BrandDesc')
    ProductSize = models.CharField(max_length=255, db_column='ProductSize')
    Currency = models.CharField(max_length=10, db_column='Currancy')
    MRP = models.FloatField(db_column='MRP')
    SellPrice = models.FloatField(db_column='SellPrice')
    Discount = models.CharField(max_length=50, db_column='Discount')
    Category = models.CharField(max_length=255, db_column='Category')

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.ProductName
