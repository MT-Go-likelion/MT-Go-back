from django.contrib import admin
from .models import teamLodgingScrap, teamRecreationScrap, teamShoppingScrap, teamSpace, teamUser
# Register your models here.

admin.site.register(teamLodgingScrap)
admin.site.register(teamRecreationScrap)
admin.site.register(teamShoppingScrap)
admin.site.register(teamUser)
admin.site.register(teamSpace)