from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('api/v1/', include('order.urls')),
    path('api/v1/', include('checks.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
