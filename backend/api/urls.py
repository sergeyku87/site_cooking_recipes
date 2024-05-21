from django.urls import include, path

import djoser.urls
import djoser.urls.authtoken
from rest_framework.routers import SimpleRouter

from users.views import UserViewSet

router_v1 = SimpleRouter()
router_v1.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]

urlpatterns += router_v1.urls

for route in router_v1.urls:
    print(route)
