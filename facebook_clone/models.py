from django.db import models
from django.contrib.auth.models import AbstractUser
from facebook_clone.manager import UserProfileManager


class UserProfile(AbstractUser):
    email = models.EmailField(unique = True, blank=False, null=True)
    profile_bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profile/pic/", blank=True, null=True)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    objects = UserProfileManager()
    username=None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class ImageUpload(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    caption = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/')


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ForeignKey(ImageUpload, on_delete=models.CASCADE, blank=True, null=True)
    caption = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(UserProfile, related_name='liked_posts', blank=True)


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    commented_on = models.DateTimeField(auto_now_add=True)



class Status(models.TextChoices):
    ACCEPTED = 'Accepted'
    PENDING = 'Pending'
    REJECTED = 'Rejected'


class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name="received_requests", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Status, default=Status.PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.from_user.first_name
