# Generated by Django 4.0.1 on 2022-04-26 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0022_remove_building_modificated_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='created_by',
            field=models.CharField(default=None, max_length=15, null=True),
        ),
    ]
