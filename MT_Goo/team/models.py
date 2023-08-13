from django.db import models
from accounts.models import CustomUser
from lodging.models import lodgingMain
from recreation.models import recreationMain
from shopping.models import shoppingMain
import uuid

class teamSpace(models.Model):
    teamToken = models.UUIDField(default=uuid.uuid4, unique=True)
    teamName = models.CharField(max_length=20)

class teamUser(models.Model):
    teamSpace = models.ForeignKey(teamSpace, on_delete=models.CASCADE, related_name="teamSpace")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")

class teamLodgingScrap(models.Model):
    teamSpace = models.ForeignKey(teamSpace, on_delete=models.CASCADE, related_name="teamSpaceLodging")
    lodging = models.ForeignKey(lodgingMain, on_delete=models.CASCADE, related_name="lodging")

class teamRecreationScrap(models.Model):
    teamSpace = models.ForeignKey(teamSpace, on_delete=models.CASCADE, related_name="teamSpaceRecreation")
    recreation = models.ForeignKey(recreationMain, on_delete=models.CASCADE, related_name="recreation")
    
class teamShoppingScrap(models.Model):
    teamSpace = models.ForeignKey(teamSpace, on_delete=models.CASCADE, related_name="teamSpaceShopping")
    item = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)