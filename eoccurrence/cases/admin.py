from django.contrib import admin

from .models import Complainant, Case, Suspect, Witness, CourtDecision, SuspectCourtRuling
# Register your models here.
admin.site.register(Suspect)
admin.site.register(CourtDecision)
admin.site.register(SuspectCourtRuling)


class WitnessInline(admin.TabularInline):
    # This inline allows adding witnesses directly from the Case admin page
    model = Case.witnesses.through
    extra = 0
    can_delete = False
    verbose_name = "Witness"
    verbose_name_plural = "Witnesses"
    fields = ('witness',)
    readonly_fields = ('witness',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # filter only for this case
        return qs.filter(case_id=self.parent_object.id)
    
    def get_formset(self, request, obj=None, **kwargs):
        self.parent_object = obj
        return super().get_formset(request, obj, **kwargs)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ("case_number", "uuid", "created_at", "deleted")
    readonly_fields = ("uuid",)
    inlines = [WitnessInline]  # <-- add this line

@admin.register(Complainant)
class ComplainantAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "uuid") # Display first name, last name, and UUID in the list view
    readonly_fields = ("uuid",)  # shows on the detail page but not editable

