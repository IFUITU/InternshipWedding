from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .serializers import *
from .models import System_Information, Gallery, City, Event, EventPlace, Service, Order
from .permissions import IsStaffOrReadOnly, IsAuthorOrReadOnly
from .filters import OrderFilter


class SystemInfoViewSet(ModelViewSet):
    queryset = System_Information.objects.all()
    serializer_class = SystemInfoSerializer
    permission_classes = [IsStaffOrReadOnly]


class GalleryViewSet(ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [IsStaffOrReadOnly]


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsStaffOrReadOnly]


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsStaffOrReadOnly]


class EventPlaceViewSet(ModelViewSet):
    queryset = EventPlace.objects.all()
    serializer_class = EventPlaceSerializer
    permission_classes = [IsStaffOrReadOnly]


class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsStaffOrReadOnly]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filterset_fields = ['event__name', 'event_place__name', 'author', 'date_wedding']
    # filterset_class = OrderFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)












