from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', include('gettingstarted.apps.api.urls')),
]
