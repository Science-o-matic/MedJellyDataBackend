from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
#                       url(r'new/', NewSightView.as_view())
                       url(r'new/', "sights.views.new")
             )
