from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from .models import Building, Inspection

# Register your models here.
admin.site.register(Building)
admin.site.register(Inspection)