from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^new/', "sights.views.new"),
    url(r'^jellyfishes.json', "sights.views.jellyfishes")
)
