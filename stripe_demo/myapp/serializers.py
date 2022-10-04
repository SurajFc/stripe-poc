from rest_framework import serializers
from .models import Product, Cart, Purchased


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("__all__")


class CartSerializer(serializers.ModelSerializer):

    product_details = serializers.SerializerMethodField()

    def get_product_details(self, obj):
        data = Product.objects.get(id=obj.product.id)
        serializer = ProductSerializer(data, many=False)
        return serializer.data

    class Meta:
        model = Cart
        fields = ("id", "product_details", "product",
                  "created_at", "updated_at")


class AddPurhcasedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchased
        fields = "__all__"

class GetPurchasedSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()

    def get_product_details(self, obj):
        data = Product.objects.get(id=obj.product.id)
        serializer = ProductSerializer(data, many=False)
        return serializer.data

    class Meta:
        model = Purchased
        fields = "__all__"