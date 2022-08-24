from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter
from django.db.models.aggregates import Count

from .models  import User
from main.models import Order


class OrderSumfilter(SimpleListFilter):
    title = 'order_sum'
    parameter_name = "order_sum"
    
    def lookups(self, request, model_admin):
        orders = Order.objects.all()
        return [(order.id, order.author) for order in orders]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(author=1)


class UserAdmin(admin.ModelAdmin):
    model = User
    # inlines = [OrderInline]
    list_display = ['phone', 'first_name', 'is_staff', 'is_blocked', 'show_order', 'date_joined']
    list_filter = ('is_staff','is_blocked',)
    search_fields = ['id', 'phone', 'first_name']

    def show_order(self, obj):
        count = Order.objects.filter(author=obj).count()
        url = str(
            reverse('admin:main_order_changelist')
            + "?"
            + urlencode({"author__id__exact":f"{obj.id}"}),
        )
        return format_html('<a href="{}">{} Orders</a>', url, count)
    show_order.short_description = "User's orders"

    def cnt_order(self, obj):
        cnt = Order.objects.filter(author=obj).count()
        return cnt

    def save_model(self, request, obj, form, change) -> None:
        print(change)
        obj.set_password(obj.password)
        print(obj.password)
        return super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
