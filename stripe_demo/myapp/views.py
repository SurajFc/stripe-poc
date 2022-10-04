import stripe
import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .serializers import (
    ProductSerializer, CartSerializer, AddPurhcasedSerializer, GetPurchasedSerializer
)
from .models import (
    Cart,
    Product,
    Purchased
)

stripe.api_key = "sk_test_51LgPpiSE3waIGV7vBdqjUAtCUY7nZe5a8tCordJzcT2C6CzWsMPu1yQ1XhUtYE97Kp9wyUBYwDlcYri2VA1YImWj005874lRsD"


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class HandleCouponView(CreateAPIView):
    """
    Class for checking coupon validation
    """

    def post(self, request, *args, **kwargs):
        """
        POST  method for getting stripe coupons and its details if present.
        """
        try:

            coupon = request.data['coupon']
            res = stripe.Coupon.retrieve(coupon)
            return Response(res, status=200)
        except Exception as e:
            return Response({"msg": "invalid coupon"}, status=400)


class StripeCheckoutView(CreateAPIView):
    """
    Class for creating api for getting stripe payment url.
    """

    def post(self, request, *args, **kwargs):
        """
        POST  method for getting stripe session url and sending ut back.
        """

        price_obj = request.data['price_obj']
        success_url = request.data['success_url']
        cancel_url = request.data['cancel_url']
        coupon = request.data.get('coupon', None)
        metadata = request.data['metadata']
        if price_obj:
            if coupon is not None:
                resp = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=price_obj,
                    mode='payment',
                    discounts=[{
                        'coupon': coupon,
                    }],
                    success_url=success_url,
                    cancel_url=cancel_url,
                    metadata=metadata
                )
            else:
                resp = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=price_obj,
                    mode='payment',
                    success_url=success_url,
                    cancel_url=cancel_url,
                    metadata=metadata
                )

            return Response(resp)

        else:
            return Response({"msg": "invalid "}, status=400)


class PaymentVerifyView(CreateAPIView):
    """
    Class for checking session payment status.
    """
    serializer_class = AddPurhcasedSerializer

    def post(self, request, *args, **kwargs):
        """
        POST  method for getting stripe session id and doing update in db accordingly.
        """
        stripe_session_id = request.data['stripe_session_id']
        resp = ""
        if stripe_session_id is not None:
            res = stripe.checkout.Session.retrieve(
                stripe_session_id
            )

            if res.status == "complete":
                resp = stripe.PaymentIntent.retrieve(
                    res.payment_intent
                )

            products = json.loads(res.metadata.products)

            for product in products:
                data = {
                    "payment_id": resp['id'],
                    "amount": product['price'],
                    "product": product['product']
                }
                serializer = self.get_serializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            Cart.objects.all().delete()

        return Response({"res": res, 'resp': resp})


class GetPurchasedProductView(viewsets.ModelViewSet):
    serializer_class = GetPurchasedSerializer
    queryset = Purchased.objects.all()
