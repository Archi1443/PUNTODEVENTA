# Generated by Django 5.0.6 on 2024-06-04 14:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cobros', '0003_venta_remove_detallecobro_cliente_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleventa',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
