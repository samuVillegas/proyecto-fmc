# Generated by Django 4.0.1 on 2022-04-16 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_rename_is_pass_building_inspection_is_inspection_successful'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='building',
            options={'ordering': ['site_name']},
        ),
    ]
