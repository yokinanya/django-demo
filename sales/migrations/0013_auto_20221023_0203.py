# Generated by Django 2.2.10 on 2022-10-22 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0012_remove_customerindent_factory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factoryindent',
            name='payment_id',
            field=models.CharField(max_length=20, verbose_name='付款单号'),
        ),
    ]
