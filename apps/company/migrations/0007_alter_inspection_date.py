# Generated by Django 4.0.1 on 2022-04-16 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_rename_pass_building_inspection_is_pass_building_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
