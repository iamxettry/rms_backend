# Generated by Django 4.2.4 on 2023-09-01 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_menuitem_calorie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='img',
        ),
    ]
