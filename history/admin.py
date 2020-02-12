from django.contrib import admin

from .models import ExchangeRateHistory, Currency


@admin.register(ExchangeRateHistory)
class AdminExchangeRateHistory(admin.ModelAdmin):
    ordering = ('-valid_from',)
    list_display = ("currency", "valid_from", "valid_until")

admin.site.register(Currency)
