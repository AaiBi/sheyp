# Generated by Django 3.2.9 on 2021-11-12 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0009_auto_20211112_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='property_type_details',
            name='garage',
            field=models.CharField(default='', max_length=5),
        ),
    ]
