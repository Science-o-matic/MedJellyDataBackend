# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Sight, Beach, VariablesGroup, Variable, MeasureUnit, SightVariables, \
    ReportingClient, City, BeachOwner, Jellyfish, JellyfishSize, JellyfishAbundance, \
    SightJellyfishes, ProteccionCivilBeach
from sights.exporters import FTPExporter


class BeachAdmin(admin.ModelAdmin):
    search_fields = ("name", "town",)


class ProteccionCivilBeachAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("code", "name", "town")

class VariableInline(admin.TabularInline):
    model = SightVariables


class JellyfishInline(admin.TabularInline):
    model = SightJellyfishes


class SightAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "beach", "reported_from", "validated",
                    "api_sent", "api_sent_timestamp")
    list_filter = ( "validated", "api_sent", "timestamp", "reported_from", "beach" )
    actions = ['mark_as_valid', 'mark_as_invalid', 'api_export']
    inlines = [VariableInline, JellyfishInline]
    date_hierarchy = 'timestamp'

    def mark_as_valid(self, request, queryset):
        queryset.update(validated=True)
    mark_as_valid.short_description = "Validar avistamientos seleccionados"

    def mark_as_invalid(self, request, queryset):
        queryset.update(validated=False)
    mark_as_invalid.short_description = "Invalidar avistamientos seleccionados"

    def api_export(self, request, queryset):
        self.mark_as_valid(request, queryset)
        for item in queryset:
            item.export()
    api_export.short_description = "Validar y exportar a MedJelly avistamientos seleccionados"

    def export(self, request, queryset):
        self.api_export(request, queryset)
    export.short_description = "Exportar avistamientos seleccionados (FTP y MedJelly)"


class SightVariablesAdmin(admin.ModelAdmin):
    fields = ("sight", "variable", "value",)
    raw_id_fields = ("variable",)


class VariableAdmin(admin.ModelAdmin):
    search_fields = ("type", "description")
    list_display = ("type", "description", "field_type")
    list_filter = ("field_type","group")


class JellyfishSizeAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


class JellyfisAbundanceAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


admin.site.register(Sight, SightAdmin)
admin.site.register(Beach, BeachAdmin)
admin.site.register(VariablesGroup)
admin.site.register(Variable, VariableAdmin)
admin.site.register(MeasureUnit)
admin.site.register(SightVariables, SightVariablesAdmin)
admin.site.register(ReportingClient)
admin.site.register(City)
admin.site.register(BeachOwner)
admin.site.register(Jellyfish)
admin.site.register(JellyfishSize, JellyfishSizeAdmin)
admin.site.register(JellyfishAbundance, JellyfishSizeAdmin)
admin.site.register(ProteccionCivilBeach, ProteccionCivilBeachAdmin)
