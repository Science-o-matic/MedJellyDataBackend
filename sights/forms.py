# -*- coding: utf-8 -*-
import json
import datetime
from django import forms
from django.forms.widgets import HiddenInput
from form_utils.forms import BetterForm
from sights.models import Sight, Variable, VariablesGroup, Beach, Jellyfish, JellyfishSize, \
    JellyfishAbundance


class SightForm(BetterForm):

    def __init__(self, *args, **kwargs):
        super(SightForm, self).__init__()

        self.user = kwargs["user"]
        self.fields = {
            'beach': forms.ModelChoiceField(
                queryset=Beach.objects.filter(users__in=(self.user,)), initial=1, label="Platja"),
            'timestamp': forms.DateTimeField(
                initial=datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                input_formats="%d-%m-%Y %H:00",
                label="Data de medició"),
            'jellyfishes_presence': forms.BooleanField(label="Presencia de medusas"),
            'jellyfishes[]': forms.ModelChoiceField(
                queryset=Jellyfish.objects.all(),
                label="Especie de medusa",
            ),
            'jellyfishes_sizes[]': forms.ModelChoiceField(
                queryset=JellyfishSize.objects.all(),
                label="Tamaño",
            ),
            'jellyfishes_abundances[]': forms.ModelChoiceField(
                queryset=JellyfishAbundance.objects.all(),
                label="Abundancia",
            ),
            'comments': forms.CharField(widget=forms.Textarea, label="Observacions")
        }

        self._append_variables_fieldsets()

        self.fieldsets.fieldsets.append(
            ('jellyfishes_presence', {'fields': ['jellyfishes_presence'], 'legend': ''})
        )
        self.fieldsets.fieldsets.append(
            ('jellyfishes', {'fields': ['jellyfishes[]', 'jellyfishes_sizes[]',
                                        'jellyfishes_abundances[]'],
                             'legend': 'Medusas',
                             'classes': ['jellyfishes']})
       )
        self.fieldsets.fieldsets.append(
            ('comments', {'fields': ['comments',],
                          'legend': 'Observacions'})
        )

    def _append_variables_fieldsets(self):
        for group in VariablesGroup.objects.all():
            variables = group.variable_set.all()
            fields = []
            for var in variables:
                field_name = "var_%s" % var.id
                self.fields[field_name] = self._field_class(var)
                fields.append(field_name)
            self.fieldsets.fieldsets.append((group.fieldset_name,
                                             {'fields': fields,
                                              'legend': group.name}))

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
