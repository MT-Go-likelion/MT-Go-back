from django.db import models
from accounts.models import CustomUser

class shoppingMain(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="userShopping")
    item = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)