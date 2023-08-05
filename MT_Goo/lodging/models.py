from django.db import models
from accounts.models import CustomUser
from datetime import datetime

def lodging_main_photo_path(instance, filename):
    # Upload the photo to a path that includes the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f'mainPhoto/{current_date}/{filename}'

def lodging_sub_photos_path(instance, filename):
    # Upload the photo to a path that includes the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f'subPhotos/{current_date}/{filename}'

class lodgingMain(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    price = models.IntegerField()
    phoneNumber = models.CharField(max_length=20)
    homePageURL = models.CharField(max_length=50)
    headCount = models.IntegerField()
    scrap = models.IntegerField(default=0)
    content = models.TextField()
    precaution = models.TextField()
    checkInTime = models.CharField(max_length=20)
    checkOutTime = models.CharField(max_length=20)
    mainPhoto = models.ImageField(upload_to=lodging_main_photo_path, blank=True, null=True)
    
    def __str__(self):
        return self.name

class lodgingPhoto(models.Model):
    image = models.ImageField(upload_to=lodging_sub_photos_path, blank=True, null=True)
    lodging = models.ForeignKey(lodgingMain, on_delete=models.CASCADE, related_name='photos')  # ForeignKey로 변경

class priceByDate(models.Model):
    lodging = models.ForeignKey(lodgingMain, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.lodging.name} - {self.date}: {self.price}"

class review(models.Model):
    score = models.DecimalField(max_digits=2, decimal_places=1)
    image = models.ImageField(upload_to="review/", null=True, blank=True)
    contents = models.TextField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lodging = models.ForeignKey(lodgingMain, on_delete=models.CASCADE)  # lodgingMain 모델과 ForeignKey로 연결
    def __str__(self):
        return f"review"

class lodgingScrap(models.Model):
    isScrap = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User 모델과 연결
    lodging = models.ForeignKey(lodgingMain, on_delete=models.CASCADE) # lodgingMain 모델과 연결
    def __str__(self):
        return f"lodgingScrap"