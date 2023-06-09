
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from compass import settings

urlpatterns = [
    path('', include('products.urls', namespace='products')),
    path('admin/', admin.site.urls),
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )