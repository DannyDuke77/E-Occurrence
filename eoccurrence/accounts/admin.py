from django.contrib import admin

from .models import Userprofile

# Register your models here.

@admin.register(Userprofile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "uuid",)
    readonly_fields = ("uuid",)
