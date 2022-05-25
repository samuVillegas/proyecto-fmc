from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from .models import Building, Inspection, Address

# Register your models here.
admin.site.register(Building)
admin.site.register(Inspection)
admin.site.register(Address)