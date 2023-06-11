from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from network.models import Posts
from .models import Order
import stripe
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt 
from django.conf import settings 


def new_purchase(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_id = Posts.objects.get(id=post_id)
        customer = request.user
        save_purchase = Order(customer=customer, product=post_id).save()
    return HttpResponseRedirect('/mainPage/')

def cart(request):
    orders = Order.objects.filter(customer=request.user.id, paid=False, complete=False)
    return render(request, 'ecommerce/cart.html', {
        'orders': orders,
    })

def order(request):
    orders = Order.objects.filter(customer=request.user.id, paid=True, complete=False)
    return render(request, 'ecommerce/order.html', {
        'orders': orders,
    })

def finished_order(request):
    orders = Order.objects.filter(customer=request.user.id, paid=True, complete=True)
    return render(request, 'ecommerce/finished_order.html', {
        'orders': orders,
    })

# Stripe
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    

def create_checkout_session(request):
    if request.method == 'POST':
        name = request.POST.get('text_field')
        price = request.POST.get('price_field')
        domain_url = 'http://127.0.0.1:8000/ecommerce'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'rub',
                    'product_data': {
                    'name': name,
                    },
                    'unit_amount': int(float(price)) * 100,
                },
                'quantity': 1,
                }],
            mode='payment',
            success_url=domain_url + '/success',
            cancel_url=domain_url + '/cancelled',
        )

        return redirect(checkout_session.url, code=303)
    
def success_view(request):
    return render(request, 'ecommerce/success.html')

def cancelled_view(request):
    return render(request, 'ecommerce/cancelled.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)


def create_product(name, image, price, currency="rub"):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.Product.create(
    name=name,
    #images=image,
    default_price_data={
        "unit_amount": price,
        "currency": currency,
    },
    
    expand=["default_price"],
    )
