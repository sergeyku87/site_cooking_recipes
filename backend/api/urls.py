from django.urls import include, path

from rest_framework.routers import SimpleRouter

from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import UserViewSet

router_v1 = SimpleRouter()
router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register(r'recipes', RecipeViewSet, basename='recipe')
router_v1.register(r'tags', TagViewSet, basename='tag')
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
]
urlpatterns += router_v1.urls
