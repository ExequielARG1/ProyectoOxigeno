# Generated by Django 5.0 on 2024-01-04 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OxigenoGYMAPP', '0005_alter_producto_imagen1_alter_producto_imagen2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen1',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]