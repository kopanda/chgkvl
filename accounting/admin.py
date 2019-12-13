from django.contrib import admin
from .models import Currency, Rate, PaymentMethod


admin.site.register(Currency)
admin.site.register(Rate)
admin.site.register(PaymentMethod)
