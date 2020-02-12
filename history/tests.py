import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.utils.timezone import now

from .models import ExchangeRateHistory, Currency


class TestExchangeRateHistory(TestCase):
    fixtures = ['history_TESTDATA.json']

    def setUp(self):
        self.currency = Currency.objects.get(currency="USD")

    def test_adding_exchange_rate_today(self):
        adding_exchange_rate = ExchangeRateHistory.objects.create(
            currency=self.currency,
            purchase_rate=24.75,
            selling_rate=25.15,
            valid_from=now().date())

        previous_exchange_rate = ExchangeRateHistory.objects.get(
            currency=self.currency,
            valid_from=datetime.date(2020, 1, 15))

        self.assertEquals(adding_exchange_rate.valid_until, None)
        self.assertEquals(adding_exchange_rate.valid_from, now().date())
        self.assertEquals(previous_exchange_rate.valid_until,
                          adding_exchange_rate.valid_from - datetime.timedelta(days=1))

    def test_adding_exchange_rate_from_date(self):
        adding_exchange_rate = ExchangeRateHistory.objects.create(
            currency=self.currency,
            purchase_rate=24.75,
            selling_rate=25.15,
            valid_from=datetime.date(2020, 1, 10))

        previous_exchange_rate = ExchangeRateHistory.objects.get(
            currency=self.currency,
            valid_from=datetime.date(2020, 1, 3))

        self.assertEquals(adding_exchange_rate.valid_from,
                          datetime.date(2020, 1, 10))
        self.assertEquals(adding_exchange_rate.valid_until,
                          datetime.date(2020, 1, 14))
        self.assertEquals(previous_exchange_rate.valid_until,
                          datetime.date(2020, 1, 9))

    def test_remove_exchange_rate_from_date(self):
        removing_exchange_rate = ExchangeRateHistory.objects.get(
            currency=self.currency,
            valid_from=datetime.date(2020, 1, 3))
        removing_exchange_rate.delete()

        previous_exchange_rate = ExchangeRateHistory.objects.get(
            currency=self.currency,
            valid_from=datetime.date(2019, 12, 30))

        with self.assertRaises(ObjectDoesNotExist):
            ExchangeRateHistory.objects.get(
                currency=self.currency,
                valid_from=datetime.date(2020, 1, 3))
        self.assertEquals(previous_exchange_rate.valid_until,
                          datetime.date(2020, 1, 14))
