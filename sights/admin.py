# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Sight, Beach, VariablesGroup, Variable,  BeachVariable, MeasureUnit, SightVariables, \
    ReportingClient, City, BeachOwner


class BeachAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class SightVariablesInline(admin.TabularInline):
    model = Sight.variables.through
    raw_id_fields = ("variable",)


class SightAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "beach", "reported_from", "validated", "api_sent", "ftp_sent")
    list_filter = ( "validated", "api_sent", "ftp_sent", "timestamp", "reported_from", "beach" )
    inlines = [SightVariablesInline]
    actions = ['mark_as_valid', 'mark_as_invalid', 'export']

    def mark_as_valid(self, request, queryset):
        queryset.update(validated=True)
    mark_as_valid.short_description = "Validar avistamientos seleccionados"

    def mark_as_invalid(self, request, queryset):
        queryset.update(validated=False)
    mark_as_invalid.short_description = "Invalidar avistamientos seleccionados"

    def export(self, request, queryset):
        for item in queryset:
            item.export()
    export.short_description = "Exportar avistamientos seleccionados"


class SightVariablesAdmin(admin.ModelAdmin):
    fields = ("sight", "variable", "value",)
    raw_id_fields = ("variable",)


class VariableAdmin(admin.ModelAdmin):
    search_fields = ("type", "description")
    list_display = ("type", "description", "field_type")
    list_filter = ("field_type","group")


class BeachVariableAdmin(admin.ModelAdmin):
    search_fields = ("code",)
    list_display = ("code", "variable", "beach")
    list_filter = ("beach",)


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
