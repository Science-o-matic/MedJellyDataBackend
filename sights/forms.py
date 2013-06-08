# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import HiddenInput
from form_utils.forms import BetterModelForm
from sights.models import Sight, Variable


class SightForm(BetterModelForm):

    
    def __init__(self, *args, **kwargs):
        super(SightForm, self).__init__()
        variable_fields = {}
        for var in Variable.objects.all():
            try:
                print var
                FieldClass = getattr(forms, var.field_type)
                var_fields["var_%s" % var.id] = FieldClass(label=var.label)
            except:
                pass
        self.fields.update(var_fields)
        for i in range(len(self.base_fieldsets)):
            fs_fields = self.base_fieldsets[i][1]
            fs_fields['fields'].extend(
                var_fields.keys())


    class Meta:
        model = Sight
        fieldsets = [('main', {'fields': ['beach', 'timestamp',],
                                'legend': ''}),
                      ]
