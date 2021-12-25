from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import get_images, index, result

urlpatterns = [
    path('get/<str:pk>', get_images),
    path('', index, name='index'),
    path('result/<str:id>', result, name='result')
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
