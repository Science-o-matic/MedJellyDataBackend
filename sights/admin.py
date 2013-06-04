from django.contrib import admin
from models import Sight, Beach, VariablesGroup, Variable,  MeasureUnit, SightVariables


admin.site.register(Sight)
admin.site.register(Beach)
admin.site.register(VariablesGroup)
admin.site.register(Variable)
admin.site.register(MeasureUnit)
admin.site.register(SightVariables)
