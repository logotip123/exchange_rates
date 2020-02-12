from django.shortcuts import render, get_object_or_404

from .models import Currency, ExchangeRateHistory


def get_index_page(request):
    currencies = Currency.objects.all()
    return render(request, 'history/index.html', {'currencies': currencies})


def get_currency_history(request, currency_name):
    currency = get_object_or_404(Currency, currency=currency_name)
    history = ExchangeRateHistory.objects.filter(currency=currency).order_by('-valid_from')
    return render(request, 'history/currency.html', {'currency': currency,
                                                     'history': history})
