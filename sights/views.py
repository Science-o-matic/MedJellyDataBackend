from django.views.generic.edit import FormView
from sights.forms import SightForm


class NewSightView(FormView):
    template_name = "new_sight.html"
    form_class = SightForm
    success_url = '/created/'

    def form_valid(self, form):
        return super(FormView, self).form_valid(form)
