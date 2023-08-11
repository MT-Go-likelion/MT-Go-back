from django.db import models
from datetime import datetime
from accounts.models import CustomUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os

def recreation_photo_path(instance, filename):
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f'recreation/photo/{current_date}/{filename}'

class recreationMain(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    photo = models.ImageField(upload_to=recreation_photo_path, blank=True, null=True)
    headCountMin = models.IntegerField()
    headCountMax = models.IntegerField()

@receiver(pre_save, sender=recreationMain)
def delete_previous_recreation_photo(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = recreationMain.objects.get(pk=instance.pk)
            if old_instance.photo and instance.photo != old_instance.photo:
                old_instance.photo.delete(save=False)
        except recreationMain.DoesNotExist:
            pass


class recreationScrap(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="userRecreation")
    recreation = models.ForeignKey(recreationMain, on_delete=models.CASCADE, related_name="recreationScrap")
    isScrap = models.BooleanField(default=False)