# Generated by Django 4.2.4 on 2023-09-05 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_alter_menuitem_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='menu-images/'),
        ),
    ]
