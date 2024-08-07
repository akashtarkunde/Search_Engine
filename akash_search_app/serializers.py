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
                # Convert to Float
                value = float((str(getattr(instance, field, '0')).strip()))
                representation[field] = value
            except (ValueError, InvalidOperation):
                representation[field] = None
        return representation