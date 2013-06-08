from django.conf.urls.defaults import patterns, url
from sights.views import NewSightView

urlpatterns = patterns('',
                       url(r'new/', NewSightView.as_view())
             )
