from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.conf import settings


urlpatterns = patterns(
    '',  # prefix
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^', include('ella.core.urls')),
)

if getattr(settings, 'DEBUG_URLS', False):
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
