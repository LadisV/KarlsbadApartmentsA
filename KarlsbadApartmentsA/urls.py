"""
URL configuration for KarlsbadApartmentsA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.static import serve

from rooms import views as room_views
from rooms.sitemaps import StaticViewSitemap

urlpatterns = [
    # Cesta pro přepínání jazyků
    path('i18n/', include('django.conf.urls.i18n')),
]

# Lokalizované cesty
urlpatterns += i18n_patterns(
    path(_('admin/'), admin.site.urls),  # Lokalizovaný admin
    path('', room_views.home, name='home'),
    path('home/', room_views.home, name='home_alias'),
    path(_('rooms/'), room_views.room_list, name='room_list'),  # Překlad "rooms"
    path(_('room/<int:pk>/'), room_views.room_detail, name='room_detail'),
    path(_('reservation/'), room_views.reservation, name='reservation'),
    path(_('contact/'), room_views.contact, name='contact'),
    path('privacy/', TemplateView.as_view(template_name="privacy.html"), name="privacy"),
    path('terms/', TemplateView.as_view(template_name="terms.html"), name="terms"),
    path(_('reserve/<int:room_id>/'), room_views.reserve_room, name='reserve_room'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemap}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    re_path(r'^robots\.txt$', serve, {'path': 'robots.txt', 'document_root': settings.STATIC_ROOT}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

sitemaps = {
    'static': StaticViewSitemap,
}


handler404 = 'rooms.views.custom_page_not_found'
handler500 = 'rooms.views.custom_server_error'
handler403 = 'rooms.views.custom_permission_denied'
handler400 = 'rooms.views.custom_bad_request'