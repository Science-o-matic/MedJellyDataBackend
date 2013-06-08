# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import HiddenInput
from form_utils.forms import BetterModelForm
from sights.models import Sight, Variable


class SightForm(BetterModelForm):

    class Meta:
        model = Sight
        fieldsets = [('main', {'fields': ['beach', 'timestamp',],
                               'legend': ''}),
                      ]
