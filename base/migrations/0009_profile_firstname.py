# Generated by Django 4.0.6 on 2023-06-06 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_cartitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='firstname',
            field=models.CharField(default=False, max_length=50),
        ),
    ]
