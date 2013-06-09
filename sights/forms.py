# -*- coding: utf-8 -*-
import json
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
                if var.field_type == "ChoiceField":
                    choices = [(value, value) for value in json.loads(var.possible_values)]
                    field_class = FieldClass(label=var.label, choices=choices)
                else:
                    field_class = FieldClass(label=var.label)
                self.fields[field_name] = field_class
                fieldset_fields.append(field_name)
            self.fieldsets.fieldsets.append((group.fieldset_name, 
                                             {'fields': fieldset_fields,
                                              'legend': group.name})
                                            )

    class Meta:
        model = Sight
        fieldsets = [('main', {'fields': ['beach', 'timestamp',],
                                'legend': ''}),
                      ]
