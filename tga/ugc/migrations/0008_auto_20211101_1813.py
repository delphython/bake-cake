# Generated by Django 2.2.7 on 2021-11-01 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0007_auto_20211031_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderstatuses',
            name='status',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='Статус заказа'),
        ),
    ]
