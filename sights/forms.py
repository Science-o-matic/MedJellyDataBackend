# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import HiddenInput
from form_utils.forms import BetterModelForm
from sights.models import Sight, Variable


class SightForm(BetterModelForm):

    
    def __init__(self, *args, **kwargs):
        super(SightForm, self).__init__()
        variable_fields = {}
        for variable in Variable.objects.all():
            try:
                FieldClass = getattr(forms, variable.field_type)
                variable_fields["variable_%s" % variable.id] = FieldClass(label=variable.label)
            except:
                pass
        self.fields.update(variable_fields)
        for i in range(len(self.base_fieldsets)):
            fs_fields = self.base_fieldsets[i][1]
            fs_fields['fields'].extend(
                variable_fields.keys())


    class Meta:
        model = Sight
        fieldsets = [('main', {'fields': ['beach', 'timestamp',],
                                'legend': ''}),
                      ]
