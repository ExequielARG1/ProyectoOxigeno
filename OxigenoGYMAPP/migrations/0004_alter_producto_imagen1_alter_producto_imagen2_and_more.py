# Generated by Django 5.0 on 2024-01-04 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OxigenoGYMAPP', '0003_producto_imagen1_producto_imagen2_producto_imagen3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen1',
            field=models.ImageField(blank=True, null=True, upload_to='OxigenoGYMAPP/imagenes_productos/'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen2',
            field=models.ImageField(blank=True, null=True, upload_to='OxigenoGYMAPP/imagenes_productos/'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen3',
            field=models.ImageField(blank=True, null=True, upload_to='OxigenoGYMAPP/imagenes_productos/'),
        ),
    ]
