from django.views.generic.edit import FormView
from sights.forms import SightForm
from sights.models import Sight
from django.shortcuts import render
from django.http import HttpResponseRedirect


def new(request):
    if request.method == 'POST':
        form = SightForm(request.POST, user=31)
        if form.is_valid():
            # TODO: Form validation and/or bounding next to be fixed
            # Harcoded by now
            for key, value in request.POST.iteritems():
                if key.startswith("var"):
                    # save sight variable
                    pass
                else:
                    _save_beach_attr(key, value)
                    
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


def _save_beach_attr(key, value):
    print "saving value", key, value
    if value is not None:
        sight = Sight()
        setattr(sight, key, value)
        sight.save()
