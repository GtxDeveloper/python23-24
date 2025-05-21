from django.db import models

# Create your models here.

class Home(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('unisex', 'Unisex'),
    ]
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    gender = models.CharField(max_length=10, choices=CATEGORY_CHOICES, blank=True, null=True)
    imgUrl = models.ImageField(upload_to='products/', blank=True, null=True)

class ProductInfo(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='info')
    description = models.TextField()
    category = models.CharField(max_length=100)
    bigImgUrl = models.ImageField(upload_to='products/', blank=True, null=True)

class ProductStatistics(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='statistics')
    salesPerMonth = models.IntegerField()
