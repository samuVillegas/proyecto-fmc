# Generated by Django 4.0.1 on 2022-04-17 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0012_alter_building_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='inspections',
        ),
        migrations.AddField(
            model_name='inspection',
            name='building',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.building'),
        ),
    ]