# Generated by Django 4.0.6 on 2023-06-06 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='firstname',
            field=models.CharField(default='waga', max_length=50),
        ),
    ]