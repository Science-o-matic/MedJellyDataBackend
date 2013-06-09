import datetime
import dateutil.parser
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from sights.forms import SightForm
from sights.models import Sight, Beach, ReportingClient, SightVariables, BeachVariable
from tokenapi.decorators import token_required


def new(request):
    if request.method == 'POST':
        form = SightForm(request.POST, user=31)
        if form.is_valid():
            # TODO: Form validation and/or bounding to be fixed
            # Harcoded by now
            sight = Sight()
            for key, value in request.POST.iteritems():
                if not key.startswith("var"):
                    _add_sight_attr(sight, key, value)
            sight.reported_from = ReportingClient.objects.get(id=1)
            sight.save()

            for key, value in request.POST.iteritems():
                if key.startswith("var"):
                    var_id = key.split("_")[1]
                    _add_sight_var(sight, var_id, value)

            return HttpResponseRedirect('/created/')
        else:
            print "KO"
            print form.errors
    else:
        form = SightForm({}, user=31) # An unbound form

    return render(request, 'new_sight.html', {
        'form': form,
    })


def _add_sight_attr(sight, key, value):
    if value is not None:
        if key == "beach":
            value = Beach.objects.get(pk=value)
        elif key == "timestamp":
            value = dateutil.parser.parse(value)
        setattr(sight, key, value)


def _add_sight_var(sight, var_id, value):
    beach_variable = BeachVariable.objects.get(beach=sight.beach,
                                                variable_id=var_id)
    var_type = beach_variable.variable.field_type
    SightVariables.objects.create(sight=sight,
                                  variable=beach_variable,
                                  value=_clean_value(value, var_type))

def _clean_value(value, var_type):
    if var_type == "BooleanField" and value == "on":
        return 1
    elif var_type == "DecimalField":
        return float(value)
    else:
        return int(value)
    
