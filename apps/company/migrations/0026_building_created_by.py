# Generated by Django 4.0.1 on 2022-04-28 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0025_remove_building_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='created_by',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
