# Generated by Django 4.0.1 on 2022-04-28 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0026_building_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='modificated_by',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]