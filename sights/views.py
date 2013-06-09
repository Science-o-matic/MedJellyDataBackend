import datetime
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from sights.forms import SightForm
from sights.models import Sight, Beach, ReportingClient
from tokenapi.decorators import token_required


def new(request):
    if request.method == 'POST':
        form = SightForm(request.POST, user=31)
        if form.is_valid():
            # TODO: Form validation and/or bounding to be fixed
            # Harcoded by now
            sight = Sight()
            for key, value in request.POST.iteritems():
                if key.startswith("var"):
                    # save sight variable
                    pass
                else:
                    _add_sight_attr(sight, key, value)
            sight.reported_from = ReportingClient.objects.get(id=1)
            sight.save()
            return HttpResponseRedirect('/created/')
        else:
            print "KO"
            print "form errors"
            print form.errors
    else:
        form = SightForm({}, user=31) # An unbound form

    return render(request, 'new_sight.html', {
        'form': form,
    })


def _add_sight_attr(sight, key, value):
    print "saving value", key, value
    if value is not None:
        if key == "timestamp":
            value = datetime.datetime.strptime(value, "%d-%m-%Y %H:%I")
        if key == "beach":
            value = Beach.objects.get(pk=value)
        setattr(sight, key, value)
