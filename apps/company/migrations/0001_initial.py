# Generated by Django 4.0.1 on 2022-05-19 02:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('site_name', models.CharField(max_length=50, unique=True)),
                ('address', models.CharField(max_length=70)),
                ('contact_email', models.CharField(max_length=40)),
                ('contact_mobile_number', models.PositiveIntegerField()),
                ('site_type', models.CharField(default=None, max_length=3, null=True)),
                ('regulation', models.CharField(default=None, max_length=7, null=True)),
                ('created_by', models.CharField(default=None, max_length=20)),
                ('modificated_by', models.CharField(default=None, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(default=None, max_length=1000, null=True)),
                ('is_inspection_successful', models.BooleanField(default=None, null=True)),
                ('inspected_by', models.CharField(default=None, max_length=20)),
                ('site_type', models.CharField(default=None, max_length=3, null=True)),
                ('building', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.building')),
            ],
        ),
    ]
