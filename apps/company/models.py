import uuid
from django.db import models

# Create your models here.
class Building(models.Model):
    code=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    site_name=models.CharField(max_length=50)
    address=models.CharField(max_length=70)
    contact_email=models.CharField(max_length=40)
    contact_mobile_number=models.PositiveIntegerField()
    site_type=models.CharField(max_length=3,unique=True, null=True, default=None)
