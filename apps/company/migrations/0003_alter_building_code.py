# Generated by Django 4.0.1 on 2022-02-27 03:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_alter_building_site_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='code',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
