from django.contrib import admin
from models import Sight, Beach, VariablesGroup, VariableType, VariableDescription, MeasureUnits, \
    SightVariables


admin.site.register(Sight)
admin.site.register(Beach)
admin.site.register(VariablesGroup)
admin.site.register(VariableType)
admin.site.register(VariableDescription)
admin.site.register(MeasureUnits)
admin.site.register(SightVariables)
