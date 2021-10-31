# Generated by Django 2.2.7 on 2021-10-31 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0006_auto_20211031_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customers', to='ugc.Customers', verbose_name='Заказчик'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='statuses', to='ugc.OrderStatuses', verbose_name='Статус заказа'),
        ),
    ]