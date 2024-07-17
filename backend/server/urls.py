from rest_framework.routers import DefaultRouter
from .views import ServerListViewSet, CategoryListViewSet, ServerViewSet

router = DefaultRouter()

router.register('select', ServerListViewSet, basename='server')
router.register('category', CategoryListViewSet, basename='category')
router.register("add", ServerViewSet, basename="server_add")

urlpatterns = router.urls
