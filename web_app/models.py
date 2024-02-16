from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):

    # friends = models.ManyToManyField("UserProfile",blank=True)
    password = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to="profile/pic/",blank=True,null=True)  

    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class ImageForm(models.Model):
    # user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    username = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=True,null=True)
    caption = models.CharField(max_length=100,blank=True,null=True)
    imagefield = models.ImageField(upload_to='image',blank=True,null=True)


    def get_username(self):
        if self.username:
            return f"{self.username.first_name} {self.username.last_name}"
        return ""
    

class Feeds(models.Model):
    user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,blank=True)
    image_post = models.ImageField(upload_to='post/image',blank=True,null=True)
    comment = models.CharField(max_length=2000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_comment',blank=True,null=True)



class Friend_Request(models.Model):
    from_user = models.ForeignKey(UserProfile,related_name="from_user" ,on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile,related_name="to_user",on_delete=models.CASCADE)
    


    
    