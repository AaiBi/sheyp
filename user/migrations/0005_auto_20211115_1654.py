# Generated by Django 3.2.9 on 2021-11-15 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_property_projet_tracker_property_projet_tracker_offer_property_projet_tracker_offer_image_property_p'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property_projet_tracker_offer',
            name='property_project_tacker',
        ),
        migrations.RemoveField(
            model_name='property_projet_tracker_offer_image',
            name='property_project_tracker_offer',
        ),
        migrations.RemoveField(
            model_name='property_projet_tracker_offer_payment',
            name='property_project_tracker_offer',
        ),
        migrations.RemoveField(
            model_name='property_projet_tracker_payment_image',
            name='property_project_tracker_payment',
        ),
        migrations.DeleteModel(
            name='Property_Projet_Tracker',
        ),
        migrations.DeleteModel(
            name='Property_Projet_Tracker_Offer',
        ),
        migrations.DeleteModel(
            name='Property_Projet_Tracker_Offer_Image',
        ),
        migrations.DeleteModel(
            name='Property_Projet_Tracker_Offer_Payment',
        ),
        migrations.DeleteModel(
            name='Property_Projet_Tracker_Payment_Image',
        ),
    ]
