from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from cloudinary.models import CloudinaryField

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=25,blank=True,null=True) 
    def __str__(self):
        return self.name
    
class Brand(BaseModel):
    name = models.CharField(max_length=25,blank=True,null=True)
    image = CloudinaryField("brand_image",folder='brand_image',blank=True,null=True)
    def __str__(self):
        return self.name
    
class Product(BaseModel):
    name = models.CharField(max_length=25,blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    details = models.TextField(blank=True,null=True)
    price = models.IntegerField()
    image = CloudinaryField("product_image",folder='product_image',blank=True,null=True)
    slug = AutoSlugField(populate_from='name',unique=True,null=True,default=None)
    def __str__(self):
        return self.name
    
class Cart(BaseModel):
    cart_code = models.CharField(max_length= 11,unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.cart_code}-{self.user}"
    
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity}x{self.Product} in cart {self.cart}"