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

class Inspection(models.Model):
    code=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    date = models.DateTimeField(auto_now=True)
    description=models.CharField(max_length=250)
    is_inspection_successful=models.BooleanField()
    building = models.ForeignKey(to=Building, on_delete=models.CASCADE, null=True)
    #Inspector de tipo Inspector (es quien realiza la inspeccion)