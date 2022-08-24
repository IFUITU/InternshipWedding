from django.contrib import admin
from .models import Service, Order, City, EventPlace, Event, System_Information, Gallery



class ImageInline(admin.TabularInline):
    model = Gallery


admin.site.register(City)
admin.site.register(System_Information)
admin.site.register(EventPlace)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Gallery)


class EventAdmin(admin.ModelAdmin):
        inlines = [ImageInline]

admin.site.register(Event, EventAdmin)