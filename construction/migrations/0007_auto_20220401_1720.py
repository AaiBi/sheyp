# Generated by Django 3.2.9 on 2022-04-01 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0006_auto_20220401_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='architecture_image',
            name='construction_project',
        ),
        migrations.DeleteModel(
            name='Construction_Service',
        ),
        migrations.DeleteModel(
            name='Architecture_Image',
        ),
    ]
