# Generated by Django 3.1.4 on 2021-10-31 20:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress', models.CharField(default='', max_length=200)),
                ('floor_level', models.IntegerField()),
                ('area', models.IntegerField(default=0)),
                ('aditionnal_info', models.TextField(blank=True, default='')),
                ('number_shared_bathroom', models.IntegerField()),
                ('number_private_bathroom', models.IntegerField(default=0)),
                ('number_living_room', models.IntegerField(default=0)),
                ('number_bedroom', models.IntegerField(default=0)),
                ('number_kitchen', models.IntegerField(default=0)),
                ('closette', models.CharField(default='', max_length=5)),
                ('terace', models.CharField(default='', max_length=5)),
                ('balcony', models.CharField(default='', max_length=5)),
                ('rent_price', models.IntegerField(blank=True, default=0)),
                ('sale_price', models.IntegerField(blank=True, default=0)),
                ('minimum_price', models.IntegerField(blank=True, default=0)),
                ('maximum_price', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress', models.CharField(default='', max_length=200)),
                ('number_shared_bathroom', models.IntegerField()),
                ('number_private_bathroom', models.IntegerField(default=0)),
                ('number_living_room', models.IntegerField(default=0)),
                ('number_bedroom', models.IntegerField(default=0)),
                ('number_kitchen', models.IntegerField(default=0)),
                ('area', models.IntegerField()),
                ('closette', models.CharField(default='', max_length=5)),
                ('garage', models.CharField(default='', max_length=5)),
                ('aditionnal_info', models.TextField(blank=True)),
                ('terace', models.CharField(default='', max_length=5)),
                ('rent_price', models.IntegerField(blank=True, default=0)),
                ('sale_price', models.IntegerField(blank=True, default=0)),
                ('minimum_price', models.IntegerField(blank=True, default=0)),
                ('maximum_price', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Land_Paper_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Land_Plan_Situation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Land_Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('statut', models.CharField(default='In progress', max_length=15)),
                ('accepted', models.BooleanField(default=0)),
                ('done', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Land_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(default='', max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('statut', models.BooleanField(default=1)),
                ('done', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Property_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Real_Estate_Projet_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress', models.CharField(default='', max_length=200)),
                ('private_bathroom', models.CharField(default='', max_length=5)),
                ('shared_bathroom', models.CharField(default='', max_length=5)),
                ('shared_kitchen', models.CharField(default='', max_length=5)),
                ('shared_closette', models.CharField(default='', max_length=5)),
                ('area', models.IntegerField(default=0)),
                ('rent_price', models.IntegerField(blank=True, default=0)),
                ('minimum_rent_price', models.IntegerField(blank=True, default=0)),
                ('maximum_rent_price', models.IntegerField(blank=True, default=0)),
                ('aditionnal_info', models.TextField(blank=True, default='')),
                ('property', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.property')),
            ],
        ),
        migrations.CreateModel(
            name='Service_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress', models.CharField(default='', max_length=200)),
                ('floor_level', models.IntegerField()),
                ('area', models.IntegerField()),
                ('aditionnal_info', models.TextField(blank=True)),
                ('closette', models.CharField(default='', max_length=5)),
                ('terace', models.CharField(default='', max_length=5)),
                ('balcony', models.CharField(default='', max_length=5)),
                ('rent_price', models.IntegerField(blank=True, default=0)),
                ('sale_price', models.IntegerField(blank=True, default=0)),
                ('minimum_price', models.IntegerField(blank=True, default=0)),
                ('maximum_price', models.IntegerField(blank=True, default=0)),
                ('property', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.property')),
            ],
        ),
        migrations.CreateModel(
            name='Studio_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='real_estate/images/studio/')),
                ('studio', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.studio')),
            ],
        ),
        migrations.CreateModel(
            name='Room_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='real_estate/images/room/')),
                ('room', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.room')),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='property_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='real_estate.property_type'),
        ),
        migrations.AddField(
            model_name='property',
            name='real_estate_project_type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.real_estate_projet_type'),
        ),
        migrations.AddField(
            model_name='property',
            name='service_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='real_estate.service_type'),
        ),
        migrations.AddField(
            model_name='property',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Lands',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(default='', max_length=200)),
                ('adress', models.CharField(default='0', max_length=200)),
                ('area', models.IntegerField(default='0')),
                ('additional_info', models.TextField(blank=True, default='0')),
                ('price', models.CharField(default=0, max_length=100)),
                ('minimum_price', models.CharField(default='0', max_length=100)),
                ('maximum_price', models.CharField(default='0', max_length=100)),
                ('land_paper_type', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.land_paper_type')),
                ('land_plan_situation', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.land_plan_situation')),
                ('land_project', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.land_project')),
            ],
        ),
        migrations.CreateModel(
            name='Land_Purchase_Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('land_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='real_estate.lands')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Land_Propostion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, default='0', max_length=200)),
                ('area', models.IntegerField(blank=True, default='0')),
                ('land_plan_situation', models.CharField(blank=True, default='0', max_length=100)),
                ('additional_info', models.TextField(blank=True, default='0')),
                ('price', models.CharField(default='0', max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('land_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='real_estate.lands')),
            ],
        ),
        migrations.AddField(
            model_name='land_project',
            name='land_type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.land_type'),
        ),
        migrations.AddField(
            model_name='land_project',
            name='real_estate_project_type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.real_estate_projet_type'),
        ),
        migrations.AddField(
            model_name='land_project',
            name='service_type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.service_type'),
        ),
        migrations.AddField(
            model_name='land_project',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Land_Images2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='real_estate/images/')),
                ('land_proposition', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.land_propostion')),
            ],
        ),
        migrations.CreateModel(
            name='Land_Images1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='', upload_to='real_estate/images/land/')),
                ('land', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.lands')),
            ],
        ),
        migrations.CreateModel(
            name='House_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='real_estate/images/house/')),
                ('house', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.house')),
            ],
        ),
        migrations.AddField(
            model_name='house',
            name='property',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.property'),
        ),
        migrations.CreateModel(
            name='Apartment_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='real_estate/images/apartment/')),
                ('apartment', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.apartment')),
            ],
        ),
        migrations.AddField(
            model_name='apartment',
            name='property',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='real_estate.property'),
        ),
    ]
