from rest_framework import serializers
from .models import Currency, Rate, PaymentMethod


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'
