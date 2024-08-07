from django_elasticsearch_dsl import Document, Index, fields
from .models import Product
from bson import ObjectId

product_index = Index('products')

@product_index.doc_type
class ProductDocument(Document):
    ProductName = fields.TextField(attr='ProductName')
    BrandName = fields.TextField(attr='BrandName')
    BrandDesc = fields.TextField(attr='BrandDesc')
    ProductSize = fields.TextField(attr='ProductSize')
    Currency = fields.TextField(attr='Currency')
    MRP = fields.FloatField(attr='MRP')
    SellPrice = fields.FloatField(attr='SellPrice')
    Discount = fields.FloatField(attr='Discount')
    Category = fields.TextField(attr='Category')

    class Django:
        model = Product

    def prepare(self, instance):
        data = super().prepare(instance)
        # Handle _id conversion in a different manner if needed
        if isinstance(instance._id, ObjectId):
            data['_id'] = str(instance._id)
        else:
            data['_id'] = instance._id
        return data
