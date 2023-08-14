from django.contrib import admin
from .models import Payment, Order, OrderedItem

class OrderedItemOnline(admin.TabularInline):
    model = OrderedItem
    readonly_fields = ['order', 'payment', 'user','menuitem', 'quantity', 'price', 'amount']
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method', 'status', 'order_placed_to', 'is_ordered']
    inlines = [OrderedItemOnline]


# Register your models here.
admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedItem)

