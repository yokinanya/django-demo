# Generated by Django 2.2.10 on 2022-10-22 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0011_auto_20221023_0029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerindent',
            name='factory',
        ),
    ]
