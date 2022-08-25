from rest_framework.routers import DefaultRouter
from main.views import SystemInfoViewSet, GalleryViewSet, CityViewSet, EventViewSet, EventPlaceViewSet, ServiceViewSet, OrderViewSet
from client.views import UserViewSet




router = DefaultRouter()


#MAIN APP
router.register("system-info", SystemInfoViewSet, basename='system-info')
router.register("gallery", GalleryViewSet, basename="gallery")
router.register("city", CityViewSet, basename='city')
router.register("event", EventViewSet, basename="event")
router.register("event-place", EventPlaceViewSet, basename="event-place")
router.register("service", ServiceViewSet, basename="service")
router.register("order", OrderViewSet, basename="order")


#CLIENT APP
router.register("client", UserViewSet, basename='client-viewset')
# router.register("")
# router.register("")
# router.register("")
# router.register("")
# router.register("")