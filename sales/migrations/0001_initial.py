# Generated by Django 2.2.10 on 2022-10-21 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerIndent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='数量')),
                ('track_num', models.CharField(blank=True, max_length=20, null=True, verbose_name='快递单号')),
                ('income', models.FloatField(null=True, verbose_name='收款金额')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, '已付款'), (1, '已完成')], default=0, verbose_name='订单状态')),
            ],
            options={
                'verbose_name': '客户订单',
                'db_table': 'indent_customer',
            },
        ),
        migrations.CreateModel(
            name='CustomerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='姓名')),
                ('sex', models.IntegerField(choices=[(0, '男'), (1, '女')], default=0, verbose_name='性别')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='电话')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='地址')),
                ('vip_level', models.IntegerField(blank=True, null=True, verbose_name='VIP等级')),
            ],
            options={
                'verbose_name': '客户信息',
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='FactoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='工厂名')),
                ('address', models.CharField(max_length=100, verbose_name='地址')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='联系电话')),
            ],
            options={
                'verbose_name': '工厂信息',
                'db_table': 'factory',
            },
        ),
        migrations.CreateModel(
            name='GoodsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='商品名称')),
                ('price', models.FloatField(verbose_name='价格')),
                ('types', models.CharField(max_length=100, verbose_name='类别')),
                ('brand', models.CharField(max_length=100, verbose_name='品牌')),
                ('specs', models.CharField(max_length=100, verbose_name='规格')),
                ('color', models.CharField(max_length=100, verbose_name='颜色')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('factory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.FactoryModel')),
            ],
            options={
                'verbose_name': '商品信息',
                'db_table': 'goods',
            },
        ),
        migrations.CreateModel(
            name='FeedBackIndent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300, verbose_name='反馈内容')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, '回访'), (1, '投诉')], default=0, verbose_name='状态')),
                ('customer_indent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.CustomerIndent')),
            ],
            options={
                'verbose_name': '售后反馈单',
                'db_table': 'indent_feedback',
            },
        ),
        migrations.CreateModel(
            name='FactoryIndent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.IntegerField(verbose_name='付款单号')),
                ('numbers', models.IntegerField(verbose_name='数量')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, '已提交'), (1, '已完成')], default=0, verbose_name='订单状态')),
                ('factory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.FactoryModel')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.GoodsModel')),
            ],
            options={
                'verbose_name': '工厂订单',
                'db_table': 'indent_Factory',
            },
        ),
        migrations.AddField(
            model_name='customerindent',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.CustomerModel'),
        ),
        migrations.AddField(
            model_name='customerindent',
            name='factory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.FactoryModel'),
        ),
        migrations.AddField(
            model_name='customerindent',
            name='good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.GoodsModel'),
        ),
    ]
