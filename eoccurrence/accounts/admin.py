from django.contrib import admin

from .models import Userprofile

# Register your models here.

@admin.register(Userprofile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "uuid", "is_active")
    readonly_fields = ("uuid",)
