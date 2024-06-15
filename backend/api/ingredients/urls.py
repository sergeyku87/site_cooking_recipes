from rest_framework.routers import SimpleRouter

from api.ingredients.views import IngredientViewSet

router_v1_ingredients = SimpleRouter()
router_v1_ingredients.register(
    r'ingredients',
    IngredientViewSet,
    basename='ingredient'
)
