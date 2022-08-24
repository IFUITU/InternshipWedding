from django.urls import path
from .views import OrderELKView

app_name = "search"

urlpatterns = [
    path("order/<str:query>/", OrderELKView.as_view(), name="order-search"),

]

