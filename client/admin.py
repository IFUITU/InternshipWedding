from django.contrib import admin
from .models  import User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['phone', 'first_name', 'date_joined']

admin.site.register(User, UserAdmin)
