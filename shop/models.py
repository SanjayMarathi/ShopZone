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