from django.urls import path
from rest_framework import routers
from .views import (
    ProductViewSet, CartViewSet, HandleCouponView, StripeCheckoutView, PaymentVerifyView, GetPurchasedProductView
)


router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'cart', CartViewSet)
router.register(r'purchased', GetPurchasedProductView)

urlpatterns = [
    path("coupon/", HandleCouponView.as_view()),
    path("checkout/", StripeCheckoutView.as_view()),
    path("paymentVerify/", PaymentVerifyView.as_view())
] + router.urls
