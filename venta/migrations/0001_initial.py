# Generated by Django 4.2.5 on 2023-09-27 20:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('identy', models.CharField(max_length=10)),
                ('number_phone', models.CharField(max_length=10)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
                'db_table': 'client',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=205)),
                ('number_phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'the vendor',
                'verbose_name_plural': 'vendors',
                'db_table': 'vendor',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField(default=1, verbose_name='stock')),
                ('category', models.ForeignKey(default='category', on_delete=django.db.models.deletion.CASCADE, to='venta.category')),
                ('vendor', models.ForeignKey(default='vendor', on_delete=django.db.models.deletion.CASCADE, to='venta.vendor')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.product')),
            ],
            options={
                'verbose_name': 'offer',
                'verbose_name_plural': 'offers',
                'db_table': 'offer',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=10, unique=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('client', models.ForeignKey(default='elige', on_delete=django.db.models.deletion.CASCADE, to='venta.client')),
                ('product', models.ManyToManyField(to='venta.product')),
            ],
        ),
    ]
