from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^new/', "sights.views.new", name="new_sighting"),
    url(r'^jellyfishes.json', "sights.views.jellyfishes")
)
