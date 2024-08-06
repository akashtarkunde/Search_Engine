from rest_framework import serializers
from .models import Product
from decimal import Decimal, InvalidOperation


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field in ['MRP', 'SellPrice']:
            try:
                # Convert to Decimal
                value = Decimal(str(getattr(instance, field, '0')).strip())
                representation[field] = value
            except (ValueError, InvalidOperation):
                # Handle the invalid value by setting it to None or a default value
                representation[field] = None
        return representation