# Generated by Django 4.2.4 on 2023-09-03 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_menuitem_img_alter_menuitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='img',
            field=models.ImageField(upload_to='menu-images/'),
        ),
    ]
