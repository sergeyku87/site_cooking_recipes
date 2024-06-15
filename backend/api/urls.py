from django.views.generic import TemplateView
from django.urls import include, path

from api.ingredients.urls import router_v1_ingredients
from api.recipes.urls import router_v1_recipes
from api.tags.urls import router_v1_tags
from api.users.urls import router_v1_users


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('docs/', TemplateView.as_view(
        template_name='redoc.html',
    )
    )
]
urlpatterns += router_v1_users.urls
urlpatterns += router_v1_tags.urls
urlpatterns += router_v1_recipes.urls
urlpatterns += router_v1_ingredients.urls
