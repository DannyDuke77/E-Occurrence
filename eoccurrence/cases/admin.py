from django.contrib import admin

from .models import Complainant, Case, Suspect, Witness
# Register your models here.
admin.site.register(Complainant)
admin.site.register(Case)
admin.site.register(Suspect)
admin.site.register(Witness)