# Generated by Django 5.0 on 2023-12-14 04:19

import OxigenoGYMAPP.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OxigenoGYMAPP', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='fecha_fin_cuota',
            field=models.DateField(default=OxigenoGYMAPP.models.default_fecha_fin),
        ),
        migrations.AddField(
            model_name='cliente',
            name='fecha_inicio_cuota',
            field=models.DateField(default=OxigenoGYMAPP.models.default_fecha_inicio),
        ),
    ]