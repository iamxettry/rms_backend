# Generated by Django 4.2.4 on 2023-09-08 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0005_cart_totalprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='totalPrice',
            field=models.FloatField(blank=True, null=True),
        ),
    ]