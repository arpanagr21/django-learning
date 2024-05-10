from django.shortcuts import render
from .models import Seller, Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, SellerSerializer, OrderSerializerWithData
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
from django.db.models import Prefetch

# Create your views here.
        
class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    def post(self, request):
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.error_messages,status=422)
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=204)
        


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializerWithData
    def list(self, request):
        print("helo")
        orders_with_items = Order.objects.prefetch_related('order_items').all()
        print("Number of orders with items:", len(orders_with_items))
        for order in orders_with_items:
            items = OrderItem.objects.filter(order_id=order.id)
            order.order_items.set(items)
        
        serializer = OrderSerializerWithData(orders_with_items, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        items = request.data.get('items', {})
        product_ids = list(items.keys())  
        
        products = Product.objects.filter(id__in=product_ids, is_available=True,seller_id=request.data.get('seller_id')).values('id', 'name', 'price')

        order_items = []
        total_order_amount = 0

        for product in products:
            product_id = str(product['id'])
            price = product['price']
            name = product['name']
            quantity = items.get(product_id, 0)  
            total_item_amount = price * quantity
            total_order_amount += total_item_amount

            order_items.append(OrderItem(item_name=name, item_price=price, item_quantity=quantity))

        order_data = {
            'customer_name': request.data.get('customer_name'),
            'total_amount': total_order_amount,
            'seller': request.data.get('seller_id'),  
        }
        order_serializer = OrderSerializer(data=order_data)
        
        if order_serializer.is_valid():
            order = order_serializer.save()
            for order_item in order_items:
                order_item.order = order

            OrderItem.objects.bulk_create(order_items)
            return Response({'message': 'Order created successfully'}, status=201)
        else:
            return Response(order_serializer.errors, status=400)