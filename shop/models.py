from django.db import models

class Products(models.Model):
    
    def __str__(self):
        return self.title
     
    title = models.CharField(max_length = 200)
    price = models.FloatField()
    discount_price = models.FloatField()
    category = models.CharField(max_length=200)
    description = models.TextField()
    image = models.CharField(max_length=100000)
    stock = models.IntegerField(default=10) 

# NEW MODEL ADDED FOR ORDERING DETAILS
class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, default='')
    address = models.CharField(max_length=300)
    zip_code = models.CharField(max_length=10)
    # Storing the entire cart data as JSON in the database for record keeping
    cart_data = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.name}"