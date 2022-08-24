from django.urls import path
from .views import OrderFilteredView

urlpatterns = [
    path('order/<str:date>/<str:event_placeID>/', OrderFilteredView.as_view())
]