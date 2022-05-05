import uuid
from django.db import models

# Create your models here.

class Building(models.Model):
    code=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    site_name=models.CharField(max_length=50, unique=True)
    address=models.CharField(max_length=70, unique=False)
    contact_email=models.CharField(max_length=40, unique=False)
    contact_mobile_number=models.PositiveIntegerField(unique=False)
    site_type=models.CharField(max_length=3,null=True, default=None, unique=False)
    regulation=models.CharField(max_length=7,null=True, default=None, unique=False)
    created_by=models.CharField(max_length=20, null=False, default=None, unique=False)
    modificated_by=models.CharField(max_length=20, null=True, default=None, unique=False)

class Inspection(models.Model):
    code=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    date = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=1000, null=True, default=None)
    is_inspection_successful=models.BooleanField(null=True, default=None)
    building = models.ForeignKey(to=Building, on_delete=models.CASCADE, null=True)
    inspected_by=models.CharField(max_length=20, null=False, default=None, unique=False)
