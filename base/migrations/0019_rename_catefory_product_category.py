# Generated by Django 4.0.6 on 2023-06-08 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_purchase'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='catefory',
            new_name='category',
        ),
    ]
