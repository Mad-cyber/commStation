from django.contrib import admin

from menu.models import Category, menuItem

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name','business', 'updated_at')
    search_fields = ('category_name','business__bus_name', 'updated_at') 

class menuItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('menu_title',)}
    list_display = ('menu_title', 'category','business', 'price', 'is_available', 'updated_at')
    search_fields = ('menu_title','category__category_name', 'business__bus_name', 'price') 
    list_filter = ('is_available',)



# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(menuItem, menuItemAdmin)

