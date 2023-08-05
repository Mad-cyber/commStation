from .models import Cart, Service
from menu.models import menuItem

def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items =Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else: 
                cart_count = 0

        except:
            cart_count = 0

    return dict(cart_count=cart_count)

def get_cart_amounts(request):
    subtotal = 0
    service_fee = 0
    grand_total = 0
    tax_dict = {}
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            menuitem = menuItem.objects.get(pk=item.menuitem.id)
            subtotal +=(menuitem.price * item.quantity) 

        get_service = Service.objects.filter(is_active=True)
        for i in get_service:
            service_type = i.service_type
            service_percentage = i.service_percentage
            service_amount = round((service_percentage * subtotal)/100, 2)
            tax_dict.update({service_type: {str(service_percentage): service_amount}})

        service_fee = sum(x for key in tax_dict.values() for x in key.values())
        grand_total = subtotal + service_fee

    return dict(subtotal=subtotal,service_fee=service_fee, grand_total=grand_total, tax_dict=tax_dict)

   #print(tax_dict)
    # print('service fee==>', service_fee)

        # service_fee = 0
        # for key in tax_dict.values():
        #     for x in key.values():

