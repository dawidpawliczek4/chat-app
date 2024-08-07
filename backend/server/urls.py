from rest_framework.routers import DefaultRouter
from .views import ServerListViewSet, CategoryListViewSet, ServerViewSet, ChannelViewSet

router = DefaultRouter()

router.register('select', ServerListViewSet, basename='server')
router.register('category', CategoryListViewSet, basename='category')
router.register("add", ServerViewSet, basename="server_add")
router.register("channel", ChannelViewSet, basename="channel")

urlpatterns = router.urls
