# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from models import Sight, Beach, VariablesGroup, Variable, MeasureUnit, SightVariables, \
    ReportingClient, City, BeachOwner, Jellyfish, JellyfishSize, JellyfishAbundance, \
    SightJellyfishes, ProteccionCivilBeach, MedJellyBeach
from sights.exporters import FTPExporter


class BeachAPIFilter(SimpleListFilter):
    title = 'correspondencia con API'
    parameter_name = 'api'

    def lookups(self, request, model_admin):
        return [
            ("medjelly", "Sin correspondencia en MedJelly"),
            ("proteccion_civil", "Sin correspondencia en Protección Civíl"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "medjelly":
            queryset = queryset.filter(medjelly_api_id__isnull=True)
        elif value == "proteccion_civil":
            queryset = queryset.filter(proteccion_civil_beaches__isnull=True)
        return queryset


class BeachAdmin(admin.ModelAdmin):
    search_fields = ["name",]
    list_display = ("name", "city", "medjelly_api_id", "proteccion_civil_api_id", "get_proteccion_civil_beaches")
    list_filter = (BeachAPIFilter, "city")

    def get_proteccion_civil_beaches(self, obj):
        proteccion_civil_beaches = []
        for beach in obj.proteccion_civil_beaches.all():
            proteccion_civil_beaches.append("%s (%s)" % (beach.name, beach.town))
        return ",".join(proteccion_civil_beaches)
    get_proteccion_civil_beaches.short_description = 'Playa/s Protección Civíl'


class ProteccionCivilBeachAPIFilter(SimpleListFilter):
    title = 'correspondencia con playas'
    parameter_name = 'beach'

    def lookups(self, request, model_admin):
        return [
            ("notnull", "Con correspondencia"),
            ("null", "Sin correspondencia"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "notnull":
            queryset = queryset.filter(beach__isnull=False)
        elif value == "null":
            queryset = queryset.filter(beach__isnull=True)
        return queryset


class ProteccionCivilBeachAdmin(admin.ModelAdmin):
    search_fields = ("code", "name",)
    list_display = ("code", "name",  "town", "get_beaches")
    list_filter = (ProteccionCivilBeachAPIFilter, "town",)

    def get_beaches(self, obj):
        beaches = []
        for beach in obj.beach_set.all():
            beaches.append("%s (%s)" % (beach.name, beach.city))
        return ",".join(beaches)
    get_beaches.short_description = 'Playa/s correspondiente/s'



class MedJellyBeachAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name", "town")
    list_filter = ("town",)


class VariableInline(admin.TabularInline):
    model = SightVariables


class JellyfishInline(admin.TabularInline):
    model = SightJellyfishes


class SightJellyfishPresenceFilter(SimpleListFilter):
    title = 'presencia de medusas'
    parameter_name = 'jellyfishes_presence'

    def lookups(self, request, model_admin):
        return [
            (1, "Sí"),
            (0, "No"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            value = bool(int(value))
            queryset = queryset.filter(jellyfishes_presence=value)
        return queryset

class SightAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "beach", "get_beach_city", "reported_from", "validated",
                    "api_sent", "api_sent_timestamp", "jellyfishes_presence")
    list_filter = ("validated", "api_sent", "timestamp", "reported_from",
                   SightJellyfishPresenceFilter, "beach__city", "beach",)
    actions = ['mark_as_valid', 'mark_as_invalid', 'api_export']
    inlines = [VariableInline, JellyfishInline]
    date_hierarchy = 'timestamp'

    def get_beach_city(self, obj):
        return obj.beach.city
    get_beach_city.short_description = 'Ayuntamiento'

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
admin.site.register(MedJellyBeach, MedJellyBeachAdmin)
