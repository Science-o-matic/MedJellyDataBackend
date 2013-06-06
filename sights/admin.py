from django.contrib import admin
from models import Sight, Beach, VariablesGroup, Variable,  MeasureUnit, SightVariables, \
    ReportingClient, City, BeachOwner


class BeachAdmin(admin.ModelAdmin):
    search_fields = ("name",)

admin.site.register(Sight)
admin.site.register(Beach, BeachAdmin)
admin.site.register(VariablesGroup)
admin.site.register(Variable)
admin.site.register(MeasureUnit)
admin.site.register(SightVariables)
admin.site.register(ReportingClient)
admin.site.register(City)
admin.site.register(BeachOwner)
