# Generated by Django 5.0.6 on 2024-06-25 07:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0007_accionesservicio_activo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accionesservicio',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
