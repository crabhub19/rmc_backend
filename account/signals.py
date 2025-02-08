from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import *
import cloudinary.uploader

# 1. Delete UserAccount Image When UserAccount is Deleted
@receiver(pre_delete, sender=UserAccount)
def delete_userAccount_image(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)
        
# 2. Delete Old UserAccount Image When Image is Updated
@receiver(pre_save, sender=UserAccount)
def delete_old_userAccount_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = UserAccount.objects.get(pk=instance.pk)
            if old_instance.image and str(old_instance.image) != str(instance.image):
                cloudinary.uploader.destroy(old_instance.image.public_id)
        except UserAccount.DoesNotExist:
            pass