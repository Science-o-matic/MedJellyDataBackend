# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import HiddenInput
from form_utils.forms import BetterModelForm
from sights.models import Sight, Variable, VariablesGroup


class SightForm(BetterModelForm):
    
    def __init__(self, *args, **kwargs):
        super(SightForm, self).__init__()

        fields = {}
        fieldsets = []
        for group in VariablesGroup.objects.all():
            variables = group.variable_set.all()
            fieldset_fields = []
            for var in variables:
                FieldClass = getattr(forms, var.field_type)
                field_name = "var_%s" % var.id
                fields[field_name] = FieldClass(label=var.label)
                fieldset_fields.append(field_name)
            fieldsets.append((group.fieldset_name, 
                              {'fields': fieldset_fields})
                             )
        self.fields.update(fields)
        self.base_fieldsets.extend(fieldsets)

    class Meta:
        model = Sight
        fieldsets = [('main', {'fields': ['beach', 'timestamp',],
                                'legend': ''}),
                      ]
