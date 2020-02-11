from django.db import models


class Currency(models.Model):
    currency = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.currency


class ExchangeRateHistory(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    purchase_rate = models.DecimalField(max_digits=6, decimal_places=2)
    selling_rate = models.DecimalField(max_digits=6, decimal_places=2)
    valid_from = models.DateField()
    valid_until = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = (('currency', 'valid_from'), ('currency', 'valid_until'))

    def __str__(self):
        return f"{self.currency}: {self.valid_from} - {self.valid_until}"