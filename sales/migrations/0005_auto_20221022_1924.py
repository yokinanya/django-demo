# Generated by Django 2.2.10 on 2022-10-22 11:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_auto_20221022_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customermodel',
            name='birthdate',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='生日'),
        ),
    ]
