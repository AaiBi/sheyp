# Generated by Django 3.2.9 on 2021-11-12 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0010_property_type_details_garage'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='ref',
            field=models.CharField(default='', max_length=10),
        ),
    ]
