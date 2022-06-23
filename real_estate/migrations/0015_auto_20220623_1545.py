# Generated by Django 3.2.9 on 2022-06-23 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20220623_1545'),
        ('real_estate', '0014_property_accepted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='land_images2',
            name='land_proposition',
        ),
        migrations.RemoveField(
            model_name='land_project',
            name='land_type',
        ),
        migrations.RemoveField(
            model_name='land_project',
            name='real_estate_project_type',
        ),
        migrations.RemoveField(
            model_name='land_project',
            name='service_type',
        ),
        migrations.RemoveField(
            model_name='land_project',
            name='user',
        ),
        migrations.RemoveField(
            model_name='land_propostion',
            name='land_info',
        ),
        migrations.RemoveField(
            model_name='land_purchase_order',
            name='land_info',
        ),
        migrations.RemoveField(
            model_name='land_purchase_order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='lands',
            name='land_paper_type',
        ),
        migrations.RemoveField(
            model_name='lands',
            name='land_plan_situation',
        ),
        migrations.RemoveField(
            model_name='lands',
            name='land_project',
        ),
        migrations.RemoveField(
            model_name='property',
            name='property_type',
        ),
        migrations.RemoveField(
            model_name='property',
            name='real_estate_project_type',
        ),
        migrations.RemoveField(
            model_name='property',
            name='service_type',
        ),
        migrations.RemoveField(
            model_name='property',
            name='user',
        ),
        migrations.RemoveField(
            model_name='property_type_details',
            name='property',
        ),
        migrations.RemoveField(
            model_name='property_type_details_image',
            name='property_type_detail',
        ),
        migrations.DeleteModel(
            name='Land_Images1',
        ),
        migrations.DeleteModel(
            name='Land_Images2',
        ),
        migrations.DeleteModel(
            name='Land_Paper_Type',
        ),
        migrations.DeleteModel(
            name='Land_Plan_Situation',
        ),
        migrations.DeleteModel(
            name='Land_Project',
        ),
        migrations.DeleteModel(
            name='Land_Propostion',
        ),
        migrations.DeleteModel(
            name='Land_Purchase_Order',
        ),
        migrations.DeleteModel(
            name='Land_Type',
        ),
        migrations.DeleteModel(
            name='Lands',
        ),
        migrations.DeleteModel(
            name='Property',
        ),
        migrations.DeleteModel(
            name='Property_Type',
        ),
        migrations.DeleteModel(
            name='Property_Type_Details',
        ),
        migrations.DeleteModel(
            name='Property_Type_Details_Image',
        ),
        migrations.DeleteModel(
            name='Real_Estate_Projet_Type',
        ),
        migrations.DeleteModel(
            name='Service_Type',
        ),
    ]