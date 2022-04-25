from django.contrib import admin

from .models import Building, Inspection

# Register your models here.
admin.site.register(Building)
admin.site.register(Inspection)