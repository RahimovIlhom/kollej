from django.contrib import admin
from . models import UserProfileInfo, News, HonoraryTeachers

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(News)
admin.site.register(HonoraryTeachers)
