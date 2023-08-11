from django.db import models
from accounts.models import CustomUser
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os
def lodging_main_photo_path(instance, filename):
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f'lodging/photo/mainPhoto/{current_date}/{filename}'

def lodging_sub_photos_path(instance, filename):
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f'lodging/photo/subPhotos/{current_date}/{filename}'

def lodging_review_photo_path(instance, filename):
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f'lodging/photo/reviewPhoto/{current_date}/{filename}'

class lodgingMain(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    price = models.IntegerField()
    phoneNumber = models.CharField(max_length=20)
    homePageURL = models.CharField(max_length=50)
    headCount = models.IntegerField()
    amenities = models.TextField()
    content = models.TextField()
    precaution = models.TextField()
    checkInTime = models.CharField(max_length=20)
    checkOutTime = models.CharField(max_length=20)
    mainPhoto = models.ImageField(upload_to=lodging_main_photo_path, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
@receiver(pre_save, sender=lodgingMain)
def delete_previous_main_photo(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = lodgingMain.objects.get(pk=instance.pk)
            if old_instance.mainPhoto and instance.mainPhoto != old_instance.mainPhoto:
                old_instance.mainPhoto.delete(save=False)
        except lodgingMain.DoesNotExist:
            pass

class lodgingPhoto(models.Model):
    image = models.ImageField(upload_to=lodging_sub_photos_path, blank=True, null=True)
    lodging = models.ForeignKey(lodgingMain, on_delete=models.CASCADE, related_name='photos')  # ForeignKey로 변경


@receiver(pre_save, sender=lodgingPhoto)
def delete_previous_sub_photo(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = lodgingPhoto.objects.get(pk=instance.pk)
            if old_instance.image and instance.image != old_instance.image:
                old_instance.image.delete(save=False)
        except lodgingPhoto.DoesNotExist:
            pass


class review(models.Model):
    score = models.DecimalField(max_digits=2, decimal_places=1)
    image = models.ImageField(upload_to=lodging_review_photo_path, null=True)
    contents = models.TextField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lodging = models.ForeignKey(lodgingMain, on_delete=models.CASCADE)  # lodgingMain 모델과 ForeignKey로 연결
    createdAt = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"review"
    
@receiver(pre_save, sender=review)
def delete_previous_review_photo(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = review.objects.get(pk=instance.pk)
            if old_instance.image and instance.image != old_instance.image:
                old_instance.image.delete(save=False)
        except lodgingPhoto.DoesNotExist:
            pass

class lodgingScrap(models.Model):
    isScrap = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="userLodging")  # User 모델과 연결
    lodging = models.ForeignKey(lodgingMain, on_delete=models.CASCADE, related_name="lodgingScrap") # lodgingMain 모델과 연결
    def __str__(self):
        return f"lodgingScrap"