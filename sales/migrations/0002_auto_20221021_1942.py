# Generated by Django 2.2.10 on 2022-10-21 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('job', models.CharField(blank=True, max_length=20, null=True, verbose_name='职位')),
                ('base_pay', models.FloatField(blank=True, null=True, verbose_name='基础工资')),
                ('sex', models.IntegerField(choices=[(0, '男'), (1, '女')], default=0, verbose_name='性别')),
                ('name', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='factoryindent',
            name='employees',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sales.Profile'),
        ),
        migrations.AddField(
            model_name='feedbackindent',
            name='employees',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sales.Profile'),
        ),
    ]
