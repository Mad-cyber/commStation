from django.shortcuts import render, redirect
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts
from .forms import OrderForm
from .models import Order, Payment
import simplejson as json
from django.http import JsonResponse, HttpResponse
from .utils import generate_order_number


# Create your views here.

def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('marketplace')
    
    sub_total = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['service_fee']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']
    #print(sub_total,service_fee, grand_total, tax_dict)

    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.city = form.cleaned_data['city']
            order.post_code = form.cleaned_data['post_code']
            order.country = form.cleaned_data['country']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save() # generate the id
            order.order_number = generate_order_number(order.id)
            order.save()
            context = {
                'order': order,
                'cart_items': cart_items,

            }
            return render(request, 'orders/place_order.html', context)


        else:
            print(form.errors)


    return render(request, 'orders/place_order.html')

def payments(request):
    #ensure the request is from the ajax in the place_order html file
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        #store the detials in the payment model
            order_number = request.POST.get('order_number')
            transaction_id = request.POST.get('transaction_id')
            payment_method = request.POST.get('payment_method')
            status = request.POST.get('status')
            # print( order_number, transaction_id, payment_method, status)

            order = Order.objects.get(user=request.user, order_number=order_number)
            payment = Payment(
                 user = request.user,
                 transaction_id = transaction_id,
                 payment_method = payment_method, 
                 amount = order.total,
                 status = status    
            )
            payment.save()
            #update to the order model
            order.payment = payment
            order.is_ordered = True
            order.save()
            return HttpResponse('Saved payment')


    return HttpResponse('Payments view')



