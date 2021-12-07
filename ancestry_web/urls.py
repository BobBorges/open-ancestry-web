from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import private_storage.urls

urlpatterns = [
    path('', include('public.urls')),
    path('admin/', admin.site.urls),
    path('priv/', include('private.urls')),
    path('auth/', include('authentication.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
