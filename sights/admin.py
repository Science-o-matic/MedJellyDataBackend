from django.contrib import admin
from models import Sight, Beach, VariablesGroup, Variable,  BeachVariable, MeasureUnit, SightVariables, \
    ReportingClient, City, BeachOwner


class BeachAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class SightVariablesInline(admin.TabularInline):
    model = Sight.variables.through
    raw_id_fields = ("variable",)


class SightAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "beach", "reported_from", "validated")
    list_filter = ( "validated", "timestamp", "beach")
    inlines = [SightVariablesInline]


class SightVariablesAdmin(admin.ModelAdmin):
    fields = ("sight", "variable", "value",)
    raw_id_fields = ("variable",)


class VariableAdmin(admin.ModelAdmin):
    list_display = ("type", "description", "field_type")
    list_filter = ("field_type","group") 


class BeachVariableAdmin(admin.ModelAdmin):
    pass


admin.site.register(Sight, SightAdmin)
admin.site.register(Beach, BeachAdmin)
admin.site.register(BeachVariable, BeachVariableAdmin)
admin.site.register(VariablesGroup)
admin.site.register(Variable, VariableAdmin)
admin.site.register(MeasureUnit)
admin.site.register(SightVariables, SightVariablesAdmin)
admin.site.register(ReportingClient)
admin.site.register(City)
admin.site.register(BeachOwner)
