from django.contrib import admin
from django.contrib import admin
from .models import Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display= ['user','birthday']
# Register your models here.

# Register your models here.
