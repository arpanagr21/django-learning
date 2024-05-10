from rest_framework import serializers
from .models import Seller, Product, Order, OrderItem


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

    def validate_age(self, age):
        if age < 18 or age > 50:
            raise serializers.ValidationError("Age must be between 18 and 50.")
        return age

    def validate_country(self, country):
        if country != "IN":
            raise serializers.ValidationError("We currently only allow sellers from India.")
        return country


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, price):
        if price < 100:
            raise serializers.ValidationError("We don't allow products having price less than 100")
        elif price > 1000:
            raise serializers.ValidationError("We don't allow products having price more than 1000")
        return price

    def validate_name(self, name):
        if len(name) > 10:
            raise serializers.ValidationError("Product name should not have more than 10 characters.")
        return name 


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer_name', 'total_amount', 'seller']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializerWithData(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
