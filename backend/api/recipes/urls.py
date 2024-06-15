from rest_framework.routers import SimpleRouter

from api.recipes.views import RecipeViewSet


router_v1_recipes = SimpleRouter()
router_v1_recipes.register(r'recipes', RecipeViewSet, basename='recipe')
