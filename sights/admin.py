from django.contrib import admin
from models import Sight, Beach, VariablesGroup, Variable,  BeachVariable, MeasureUnit, SightVariables, \
    ReportingClient, City, BeachOwner


class BeachAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class SightAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "beach",)
    list_filter = ("timestamp", "beach")


class VariableAdmin(admin.ModelAdmin):
    list_display = ("type", "description", "field_type")
    list_filter = ("field_type",) 


admin.site.register(Sight, SightAdmin)
admin.site.register(Beach, BeachAdmin)
admin.site.register(BeachVariable)
admin.site.register(VariablesGroup)
admin.site.register(Variable, VariableAdmin)
admin.site.register(MeasureUnit)
admin.site.register(SightVariables)
admin.site.register(ReportingClient)
admin.site.register(City)
admin.site.register(BeachOwner)
