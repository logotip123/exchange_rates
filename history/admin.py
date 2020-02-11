from django.contrib import admin

from .models import ExchangeRateHistory, Currency


admin.site.register(ExchangeRateHistory)
admin.site.register(Currency)
