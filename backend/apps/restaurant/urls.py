from rest_framework.routers import DefaultRouter
from.views import RestaurantProfileViewSet

router = DefaultRouter()
router.register("restaurant",RestaurantProfileViewSet,basename="restaurant")

urlpatterns = router.urls
    
