from django.contrib import admin
from .models import Service, Order, City, EventPlace, Event, System_Information, Gallery


admin.site.register(City)
admin.site.register(System_Information)
admin.site.register(EventPlace)
admin.site.register(Gallery)

#INLINES
class ImageInline(admin.TabularInline):
    model = Gallery


#MODEL ADMINS
class OrderAdmin(admin.ModelAdmin):
    list_display = ['author', 'location_wedding', 'status', 'date_wedding']
    list_filter = ("event", "date_wedding", 'location_wedding', 'total_price', 'author')
admin.site.register(Order, OrderAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    list_filter = ['price', 'event']
    search_fields = ("id", "price", "name")
admin.site.register(Service, ServiceAdmin)


class EventAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
admin.site.register(Event, EventAdmin)


