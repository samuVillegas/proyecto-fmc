# Generated by Django 4.0.1 on 2022-05-22 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_alter_address_full_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='address',
        ),
        migrations.AddField(
            model_name='address',
            name='building',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.building'),
        ),
    ]