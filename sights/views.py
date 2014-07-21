# -*- coding: utf-8 -*-
import datetime
import dateutil.parser
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import simplejson
from sights.forms import SightForm
from sights.models import Sight, Beach, ReportingClient, SightVariables, \
    Variable, Jellyfish, JellyfishSize, JellyfishAbundance, \
    SightJellyfishes
from sights import mailer
from tokenapi.decorators import token_required


@token_required
def new(request):
    user = request.user
    context = {}

    if request.method == 'POST':
        # TODO: Form validation and bounding must be fixed
        data  = dict(request.POST)
        attributes, variables, jellyfishes = _split_form_data(data)
        sighting = Sight()

        _add_sighting_attributes(sighting, attributes)

        _add_sighting_variables(sighting, variables)

        _add_sighting_jellyfishes(sighting, jellyfishes)

        context = {
            "message": "Dades creades correctament.",
            "form": SightForm({}, user=user)
        }

        mailer.notify_new_sighting(sighting)
    else:
        context['form'] = SightForm({}, user=user) # An unbound form

    return render(request, 'new_sight.html', context)


def _split_form_data(data):
    attributes = {}
    variables = {}
    jellyfishes = {
        "types": [jelly for jelly in data.pop("jellyfishes", []) if jelly],
        "sizes": data.pop("jellyfishes_sizes", []),
        "abundances": data.pop("jellyfishes_abundances", [])
    }

    for key, value in data.iteritems():
        if key.startswith("var"):
            variables[key] = value if len(value) > 1 else value[0]
        else:
            attributes[key] = value if len(value) > 1 else value[0]

    return (attributes, variables, jellyfishes)


def _add_sighting_attributes(sighting, attributes):
    for key, value in attributes.iteritems():
        _add_sighting_attr(sighting, key, value)
    sighting.reported_from = ReportingClient.objects.get(id=1)
    sighting.save()


def _add_sighting_variables(sighting, variables):
    for key, value in variables.iteritems():
        var_id = key.split("_")[1]
        _add_sighting_var(sighting, var_id, value)


def _add_sighting_jellyfishes(sighting, jellyfishes):
    for i, jelly_id in enumerate(jellyfishes["types"]):
        jelly_size = jellyfishes["sizes"][i] or 0
        jelly_abundance = jellyfishes["abundances"][i] or 0

        sighting.jellyfishes.add(
            SightJellyfishes(
                sight=sighting,
                jellyfish_id=jelly_id,
                size_id=jelly_size,
                abundance_id=jelly_abundance
            )
        )


def _add_sighting_attr(sighting, key, value):
    if value is not None:
        if key == "beach":
            value = Beach.objects.get(pk=value)
        elif key == "timestamp":
            value = dateutil.parser.parse(value, dayfirst=True)
        setattr(sighting, key, value)


def _add_sighting_var(sighting, var_id, value):
    if value != '':
        variable = Variable.objects.get(id=var_id)
        SightVariables.objects.create(sight=sighting,
                                      variable=variable,
                                      value=_clean_value(value, variable.field_type))

def _clean_value(value, var_type):
    if var_type == "BooleanField" and value == "on":
        cleaned_value = 1
    else:
        if var_type == "DecimalField":
            # TODO Look for a better way to do this
            # Check /home/ygneo/.virtualenvs/medjellydatabackend/local/lib/python2.7/site-packages/django/db/models/fields/__init__.py
            # Line 869, ValidationError when running to_python
            cleaned_value = value.replace(",", ".")
        else:
            cleaned_value = int(value)
    return cleaned_value


def jellyfishes(request):
    jellyfishes = {
        "types": list(Jellyfish.objects.values("id", "name")),
        "sizes": list(JellyfishSize.objects.values("id", "name")),
        "abundances": list(JellyfishAbundance.objects.values("id", "name"))
    }
    return HttpResponse(simplejson.dumps(jellyfishes))
