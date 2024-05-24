from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from users.views import UserViewSet
from users.routers import CustomRouter


router_v1 = CustomRouter()
router_v1.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
]
urlpatterns += router_v1.urls


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
