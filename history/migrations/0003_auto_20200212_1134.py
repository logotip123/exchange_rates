# Generated by Django 3.0.3 on 2020-02-12 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_auto_20200211_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangeratehistory',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchange_rate_history', to='history.Currency'),
        ),
    ]