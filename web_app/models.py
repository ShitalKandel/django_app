from django.db import models
# from django.contrib.auth.models import AbstractUser

class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)  

    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Photo(models.Model):
    # user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    # username = models.CharField(max_length=100, blank=False)
    caption = models.CharField(max_length=100)
    imagefield = models.ImageField(upload_to='image')
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)



    def __str__(self):
        return self.caption
    
    # def save(self,args, **kwargs):
    #     if not self.username:
    #         self.username = {self.user_profile.first_name}+{self.user_profile.last_name}
    #     return (Photo,self).save(*args, **kwargs)
    


    