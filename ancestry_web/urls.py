from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('public.urls')),
    path('admin/', admin.site.urls),
    path('priv/', include('private.urls')),
    path('auth/', include('authentication.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
