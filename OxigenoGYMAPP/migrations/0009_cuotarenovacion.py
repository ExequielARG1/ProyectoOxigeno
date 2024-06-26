# Generated by Django 5.0 on 2024-04-14 03:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OxigenoGYMAPP', '0008_remove_producto_imagen2_remove_producto_imagen3_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuotaRenovacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio_cuota', models.DateField(verbose_name='Fecha de inicio de cuota')),
                ('fecha_fin_cuota', models.DateField(verbose_name='Fecha de fin de cuota')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renovaciones', to='OxigenoGYMAPP.cliente')),
            ],
            options={
                'verbose_name': 'Renovación de cuota',
                'verbose_name_plural': 'Renovaciones de cuota',
            },
        ),
    ]
