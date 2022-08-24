from django_filters import rest_framework as filters
from .models import Order


class OrderFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="date_start", lookup_expr='gte')
    end_date = filters.DateFilter(field_name="date_end", lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['date_wedding', 'start_date', 'end_date']