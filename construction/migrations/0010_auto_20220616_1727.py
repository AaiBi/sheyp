# Generated by Django 3.2.9 on 2022-06-16 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0009_quote_project_materiaux_quote_project_ouvrage_quote_project_step'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mesure_Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.AlterField(
            model_name='quote_project_materiaux',
            name='mesure_unit',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='construction.mesure_unit'),
        ),
        migrations.AlterField(
            model_name='quote_project_ouvrage',
            name='mesure_unit',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='construction.mesure_unit'),
        ),
    ]