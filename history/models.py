from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError


class Currency(models.Model):
    currency = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.currency


class ExchangeRateHistory(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='exchange_rate_history')
    purchase_rate = models.DecimalField(max_digits=6, decimal_places=2)
    selling_rate = models.DecimalField(max_digits=6, decimal_places=2)
    valid_from = models.DateField()
    valid_until = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = (('currency', 'valid_from'),)

    def _change(self, for_change):
        for_change.valid_until = self.valid_from - timedelta(days=1)
        for_change.save()

    def _previous(self):
        return ExchangeRateHistory.objects.filter(currency=self.currency,
                                                  valid_from__lt=self.valid_from).latest('valid_from')

    def last(self):
        return ExchangeRateHistory.objects.filter(currency=self.currency).latest('valid_from')

    def _first(self):
        return ExchangeRateHistory.objects.filter(currency=self.currency).latest('-valid_from')

    def save(self, *args, **kwargs):
        if self.valid_until is not None and self.valid_from > self.valid_until:
            raise IntegrityError
        if not self.id:
            try:
                first = self._first()
                if first.valid_from > self.valid_from and\
                        (self.valid_until is None or first.valid_from > self.valid_until):
                    self.valid_until = first.valid_from - timedelta(days=1)
                elif first.valid_from < self.valid_from:
                    last = self.last()
                    if (last.valid_until is None or last.valid_until < self.valid_from) \
                            and last.valid_from < self.valid_from:
                        self._change(last)
                    else:
                        previous = self._previous()
                        if self.valid_until is None or previous.valid_until > self.valid_until:
                            self.valid_until = previous.valid_until
                        self._change(previous)
                else:
                    raise IntegrityError
            except ObjectDoesNotExist:
                pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self._first() != self:
            previous = self._previous()
            if previous and self != self._last():
                previous.valid_until = self.valid_until
                previous.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.currency)
