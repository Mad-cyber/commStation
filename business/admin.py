from django.contrib import admin
from business.models import Business

# Register your models here.
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('user', 'bus_name', 'bus_tax_cert', 'is_approved', 'created_at')
    list_display_links = ('user', 'bus_name')

admin.site.register(Business, BusinessAdmin)
