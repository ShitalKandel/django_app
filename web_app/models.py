from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):

    password = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to="profile/pic/",blank=True,null=True)  

    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class ImageForm(models.Model):
    # user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    username = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=True,null=True)
    caption = models.CharField(max_length=100,blank=True,null=True)
    imagefield = models.ImageField(upload_to='image',blank=True,null=True)
    # user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)


    # def __str__(self):
    #     return self.imagefield.url

    def get_username(self):
        return f"{self.username.first_name}{self.username.last_name}"

    def __str__(self):
        return self.get_username
    
    # def save(self,*args,**kwargs):
    #     if not self.user:
    #         self.user = UserProfile.objects.get(pk=request.user.pk)
    #     super().save(*args,**kwargs)
    

class Feeds(models.Model):
    user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,blank=True)
    image_post = models.ImageField(upload_to='post/image',blank=True,null=True)
    comment = models.CharField(max_length=2000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_comment',blank=True,null=True)




# class Profile_Name(UserProfile):
#     def authenticate_user(self,username=None):
#         first,last = username.split(" ",1)
#         try:
#             user = UserProfile.objects.get(first_name = first,last_name=last)
#             if user:
#                 return user
            
#         except:
#             pass
#         return None
    
#     def get_user(self,user_id):
#         try:
#             return UserProfile.objects(pk=user_id)
#         except:
#             return None
    


    