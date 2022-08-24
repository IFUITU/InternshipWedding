from rest_framework import serializers
from .models import EventPlace, System_Information, Gallery, City, Event, EventPlace, Service, Order

class SystemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = System_Information
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = EventPlace
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True)
    
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("id","author",)