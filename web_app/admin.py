from django.contrib import admin
from .models import ImageForm,UserProfile,Feeds
from django.contrib.auth.admin import UserAdmin

admin.site.register(ImageForm)
# admin.site.register(UserProfile,UserAdmin)
admin.site.register(Feeds)

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display=["email"]
# Register your models here.

