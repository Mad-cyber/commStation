from django.contrib import admin
from .models import Cart, Service

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'menuitem', 'quantity', 'updated_at')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'service_percentage', 'is_active')

admin.site.register(Cart,CartAdmin)
admin.site.register(Service, ServiceAdmin)

