from rest_framework.routers import SimpleRouter

from api.tags.views import TagViewSet


router_v1_tags = SimpleRouter()
router_v1_tags.register(r'tags', TagViewSet, basename='tag')
