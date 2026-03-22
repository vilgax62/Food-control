from rest_framework.routers import DefaultRouter
from.views import NGOProfileViewSet


router = DefaultRouter()
router.register("ngo",NGOProfileViewSet,basename="ngo")

urlpatterns = router.urls
