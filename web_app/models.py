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
    caption = models.CharField(max_length=100)
    imagefield = models.ImageField(upload_to='image')


    def __str__(self):
        return self.caption

    