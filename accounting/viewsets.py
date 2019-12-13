from rest_framework import viewsets, filters
from .models import Currency, Rate, PaymentMethod
from .serializers import CurrencySerializer, RateSerializer, PaymentMethodSerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    filter_backends = (filters.SearchFilter,)


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filter_backends = (filters.SearchFilter,)


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    filter_backends = (filters.SearchFilter,)
