# -*- coding: utf-8 -*-
import json
import datetime
from django import forms
from django.forms.widgets import HiddenInput
from form_utils.forms import BetterForm
from sights.models import Sight, Variable, VariablesGroup, Beach


class SightForm(BetterForm):

    def __init__(self, *args, **kwargs):
        super(SightForm, self).__init__()

        self.user = kwargs["user"]
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:00")
        self.fields = {
            'beach': forms.ModelChoiceField(
                queryset=Beach.objects.filter(users__in=(self.user,)), initial=1,label="Platja"),
            'timestamp': forms.DateTimeField(
                initial=current_time, input_formats="%d-%m-%Y %H:00",
                label="Data de medició"),
            'comments': forms.CharField(widget=forms.Textarea, label="Observacions")
            }

        fieldsets = []
        for group in VariablesGroup.objects.all():
            variables = group.variable_set.all()
            fieldset_fields = []
            for var in variables:
                field_name = "var_%s" % var.id
                self.fields[field_name] = self._field_class(var)
                fieldset_fields.append(field_name)
            self.fieldsets.fieldsets.append((group.fieldset_name,
                                             {'fields': fieldset_fields,
                                              'legend': group.name}))
        self.fieldsets.fieldsets.append(('comments', {'fields': ['comments',],
                                                      'legend': 'Observacions'}))

    def _field_class(self, var):
        FieldClass = getattr(forms, var.field_type)
        if var.field_type == "ChoiceField":
            choices = []
            for value in json.loads(var.possible_values):
                choices.append(tuple(value))
                field_class = FieldClass(label=var.label, choices=choices)
        else:
            field_class = FieldClass(label=var.label)
        return field_class


    def is_valid(self):
        return True

    class Meta:
        fieldsets = [('main', {'fields': ['beach', 'timestamp',],
                                'legend': ''}),
                     ]
