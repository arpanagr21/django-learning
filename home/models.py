from django.db import models

# Create your models here.


class Seller(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    country = models.CharField(max_length=2)
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    is_available = models.BooleanField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    total_amount = models.IntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    order_items = models.ManyToManyField('OrderItem', related_name='orders')
    transaction_record = models.ForeignKey('Transaction', on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.customer_name


class OrderItem(models.Model):
    item_name = models.CharField(max_length=100)
    item_price = models.IntegerField()
    item_quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name
    
class Transaction(models.Model):
    transaction_amount = models.IntegerField()
    transaction_gateway = models.CharField(max_length=100)
    related_order = models.OneToOneField('Order', null=True, on_delete=models.CASCADE, related_name='transaction')

    def __str__(self):
        return f"Transaction {self.pk}"
