from django.contrib import admin
from facebook_clone.models import UserProfile, ImageUpload, Post, Comment, FriendRequest


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'profile_bio']


@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ['user', 'caption', 'image']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'caption', 'date_posted']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'text', 'commented_on']


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'status', 'requested_at']
