from django.shortcuts import render, redirect
from marketplace.models import Cart, Service
from marketplace.context_processors import get_cart_amounts
from menu.models import menuItem
from .forms import OrderForm
from .models import Order, Payment, OrderedItem
import simplejson as json
from django.http import JsonResponse, HttpResponse
from .utils import generate_order_number
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('marketplace')
    
    businesses_id = []
    for i in cart_items:
        if i.menuitem.business.id not in businesses_id:
          businesses_id.append(i.menuitem.business.id)

    #print(businesses_id)
    #{"business_id":{"subtotal":{"tax_type": {"service_percentage": "service_amount"}}}}
    get_service = Service.objects.filter(is_active=True)
    subtotal = 0
    total_data = {}
    k = {}
    for i in cart_items:
        menuitem = menuItem.objects.get(pk=i.menuitem.id, business_id__in=businesses_id)
        b_id = menuitem.business.id
        if b_id in k:
            subtotal = k[b_id]
            subtotal += (menuitem.price * i.quantity)
            k[b_id] = subtotal
        else:
            subtotal = (menuitem.price * i.quantity)
            k[b_id] = subtotal

        #Calculate the tax_data
        tax_dict = {}
        for i in get_service:
            service_type = i.service_type
            service_percentage = i.service_percentage
            service_amount = round((service_percentage * subtotal)/100, 2)
            tax_dict.update({service_type: {str(service_percentage): str(service_amount)}})
        #print(tax_dict) Construct total data
        total_data.update({menuitem.business.id: {str(subtotal): str(tax_dict)} })
        # print(total_data)

            #k.append(b_id)
        #print(k)
        #print(menuitem, menuitem.business.id)
        # print(subtotal)

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
            order.total_data = json.dumps(total_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save() # generate the id
            order.order_number = generate_order_number(order.id)
            order.businesses.add(*businesses_id)
            order.save()
            context = {
                'order': order,
                'cart_items': cart_items,

            }
            return render(request, 'orders/place_order.html', context)


        else:
            print(form.errors)


    return render(request, 'orders/place_order.html')

@login_required(login_url='login')
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

            #move cart items to ordered services model
            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                 ordered_item = OrderedItem()
                 ordered_item.order = order
                 ordered_item.payment = payment 
                 ordered_item.user = request.user
                 ordered_item.menuitem = item.menuitem
                 ordered_item.quantity = item.quantity
                 ordered_item.price = item.menuitem.price
                 ordered_item.amount = item.menuitem.price * item.quantity #totoal amount
                 ordered_item.save()

            #return HttpResponse('Saved order items')   
    # send order confirmation email
            mail_subject = 'Thank you for ordering with the communcation station!'
            mail_template = 'orders/order_confirmation_email.html'
            context = {
                 'user': request.user, 
                 'order': order,
                 'to_email': order.email,
                 
            }
            send_notification(mail_subject, mail_template, context)
            #return HttpResponse('Order Saved and Email Sent')
    
            #send the order to the business
            mail_subject = 'IMPORTANT: Communcation Station, New Order Request!'
            mail_template = 'orders/new_order_recieved.html'
            to_emails = []
            for i in cart_items:
                 if i.menuitem.business.user.email not in to_emails:
                    to_emails.append(i.menuitem.business.user.email)
            print('to emails are equal to', to_emails)    
            context = {
                 'order': order,
                 'to_email': to_emails,
            }
            send_notification(mail_subject, mail_template, context)

            #clear cart ofter payment post order
            cart_items.delete()
            # return HttpResponse('Order Saved and Email Sent')
    
            #return back to ajax with success or failure message
            response = {
                 'order_number': order_number,
                 'transaction_id': transaction_id,
                 
            }
            return JsonResponse(response)
    return HttpResponse('payments view')

def order_complete(request):
     order_number = request.GET.get('order_no')
     transaction_id = request.GET.get('trans_id')

     try:
          order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
          ordered_item = OrderedItem.objects.filter(order=order)

          subtotal = 0
          for item in ordered_item:
              subtotal += (item.price * item.quantity)

          tax_data = json.loads(order.tax_data)
          print(tax_data)
          context= {
               'order':order,
               'ordered_item': ordered_item,
               'subtotal': subtotal,
               'tax_data': tax_data,

          }
          return render (request, 'orders/order_complete.html', context)
     except:
        
        return redirect('home')
     
     
     




