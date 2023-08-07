from django.db import models
from datetime import datetime
from accounts.models import CustomUser
def recreation_photo_path(instance, filename):
    # Upload the photo to a path that includes the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f'recreation/photo/{current_date}/{filename}'

class recreationMain(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    photo = models.ImageField(upload_to=recreation_photo_path, blank=True, null=True)
    headCountMin = models.IntegerField()
    headCountMax = models.IntegerField()
    

class recreationScrap(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="userRecreation")
    recreation = models.ForeignKey(recreationMain, on_delete=models.CASCADE, related_name="recreationScrap")
    isScrap = models.BooleanField(default=False)