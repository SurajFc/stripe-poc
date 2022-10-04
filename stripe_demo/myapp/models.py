import stripe
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

stripe.api_key = "sk_test_51LgPpiSE3waIGV7vBdqjUAtCUY7nZe5a8tCordJzcT2C6CzWsMPu1yQ1XhUtYE97Kp9wyUBYwDlcYri2VA1YImWj005874lRsD"


def create_stripe_product(data):
    return stripe.Product.create(
        name=data['product_name'],
        default_price_data={
            "currency": "USD",
            "unit_amount": data['price'] * 100
        },
        description=data['description'],
        images=[data['img_url']]
    )


class Product(models.Model):
    product_name = models.CharField(
        max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price = models.IntegerField(null=True, blank=False, default=0)
    img_url = models.TextField(null=False, blank=False)
    stripe_product = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Product, dispatch_uid="create_stripe_product")
def add_stripe_product(sender, instance, **kwargs):
    data = {
        "product_name": instance.product_name,
        "price": instance.price,
        "description": instance.description,
        "img_url": instance.img_url
    }
    stripe_product = create_stripe_product(data)
    Product.objects.filter(id=instance.id).update(
        stripe_product=stripe_product.id)


class Cart(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Purchased(models.Model):
    payment_id = models.CharField(null=False, blank=False, max_length=100)
    amount = models.FloatField(null=True, blank=False)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
