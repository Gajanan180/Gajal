from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from merchants.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('merchants/', include('merchants.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Gajal Food Admin'
admin.site.site_title = 'Gajal Food'
admin.site.index_title = 'Food Ordering Management'
