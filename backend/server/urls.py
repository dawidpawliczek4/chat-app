from rest_framework.routers import DefaultRouter
from .views import ServerListViewSet, CategoryListViewSet

router = DefaultRouter()

router.register('select', ServerListViewSet, basename='server')
router.register('category', CategoryListViewSet, basename='category')

urlpatterns = router.urls
