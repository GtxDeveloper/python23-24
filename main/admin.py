from django.contrib import admin
from .models import Home, Product, ProductInfo, ProductStatistics

# Register your models here.
admin.site.register(Home)
admin.site.register(Product)
admin.site.register(ProductInfo)
admin.site.register(ProductStatistics)