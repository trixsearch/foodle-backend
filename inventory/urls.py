from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RawMaterialViewSet, RecipeIngredientViewSet, RecipeViewSet

router = DefaultRouter()
router.register(r'raw-materials', RawMaterialViewSet, basename='rawmaterial')
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'recipe-ingredients', RecipeIngredientViewSet, basename='recipeingredient')

urlpatterns = [
    path('', include(router.urls)),
]
