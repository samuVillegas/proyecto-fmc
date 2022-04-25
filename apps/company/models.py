import uuid
from django.db import models

# Create your models here.

class Inspection(models.Model):
    code=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    date = models.DateField()
    description=models.CharField(max_length=250)
    pass_building=models.CharField(max_length=10)
    #Inspector de tipo Inspector (es quien realiza la inspeccion)

class Building(models.Model):
    code=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    site_name=models.CharField(max_length=50, unique=True)
    address=models.CharField(max_length=70, unique=False)
    contact_email=models.CharField(max_length=40, unique=False)
    contact_mobile_number=models.PositiveIntegerField(unique=False)
    site_type=models.CharField(max_length=3,null=True, default=None, unique=False)
    regulation=models.CharField(max_length=7,null=True, default=None, unique=False)
    inspections = models.ForeignKey(Inspection, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['site_name']