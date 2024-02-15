from django.contrib import admin
from .models import ImageForm,UserProfile,Feeds
from django.contrib.auth.admin import UserAdmin


# Register your models here.


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display=["email"]


admin.site.register(ImageForm)
admin.site.register(Feeds)



