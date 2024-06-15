from rest_framework.routers import SimpleRouter

from api.users.views import UserViewSet


router_v1_users = SimpleRouter()
router_v1_users.register(r'users', UserViewSet, basename='user')
