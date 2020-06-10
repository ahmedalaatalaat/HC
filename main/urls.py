from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from .admin import *
from django.conf.urls import handler400, handler403, handler404, handler500
from cpanel.views import error_400, error_403, error_404, error_500


urlpatterns = [
    path('', include('website.urls')),
    path('cpanel/', include('cpanel.urls')),
    path('ai_panel/', include('ai.urls')),
    path('browse/', include('vezeeta.urls')),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    # path('admin/', my_admin_site.urls),
    # path('my_admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    # path('my_admin/', admin.site.urls),
    path('admin/', (my_admin_site.urls)),
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = error_400
handler403 = error_403
handler404 = error_404
handler500 = error_500
