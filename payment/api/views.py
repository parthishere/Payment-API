from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAdminUser


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import stripe

    
    

class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'payment/payment.html'

    def get(self, request):
        stripe_config = {'publicKey': 'f***y**'}
        return Response({'profiles': stripe_config})
    

@api_view(['GET'])    
def stripe_config(request):
    
    return Response({ 
                     'publicKey': settings.STRIPE_PUBLISHABLE_KEY,
            })
    
    
    
# payments/views.py
@api_view(['GET'])
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'T-shirt',
                        'quantity': 1,
                        'currency': 'inr',
                        'amount': '100',
                    }
                ]
            )
            return Response({'sessionId': checkout_session['id']})
        except Exception as e:
            return Response({'error': str(e)})
        
        
class SuccessView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'payment/success.html'

    def get(self, request):
        stripe_config = {'type':'success'}
        return Response({'status': stripe_config})
    
    
class CancelledView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'payment/cencelled.html'

    def get(self, request):
        stripe_config = {'type':'cancel'}
        return Response({'status': stripe_config})