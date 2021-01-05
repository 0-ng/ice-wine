# Generated by Django 2.2.5 on 2020-12-28 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('luogu', '0002_auto_20201226_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default='在线支付', max_length=32, verbose_name='支付方式'),
        ),
        migrations.AlterField(
            model_name='sales',
            name='date',
            field=models.DateField(verbose_name='日期'),
        ),
        migrations.AlterField(
            model_name='shopping_cart_details',
            name='commodity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='luogu.Commodity'),
        ),
    ]
