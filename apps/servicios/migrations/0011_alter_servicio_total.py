# Generated by Django 5.0.6 on 2024-06-28 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0010_servicio_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
