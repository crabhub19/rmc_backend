from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import Product, Brand, Category
import cloudinary.uploader
# 1. Delete Product Image When Product is Deleted
@receiver(pre_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)

# 2. Delete Old Product Image When Image is Updated
@receiver(pre_save, sender=Product)
def delete_old_product_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Product.objects.get(pk=instance.pk)
            if old_instance.image and str(old_instance.image) != str(instance.image):
                cloudinary.uploader.destroy(old_instance.image.public_id)
        except Product.DoesNotExist:
            pass

# 3. Delete Brand Image and Associated Product Images When Brand is Deleted
@receiver(pre_delete, sender=Brand)
def delete_brand_and_products(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)  # Delete Brand Image
    products = Product.objects.filter(brand=instance)  # Get Related Products
    for product in products:
        if product.image:
            cloudinary.uploader.destroy(product.image.public_id)  # Delete Product Images

# 4. Delete Associated Product Images When Category is Deleted
@receiver(pre_delete, sender=Category)
def delete_category_products(sender, instance, **kwargs):
    products = Product.objects.filter(category=instance)  # Get Related Products
    for product in products:
        if product.image:
            cloudinary.uploader.destroy(product.image.public_id)  # Delete Product Images