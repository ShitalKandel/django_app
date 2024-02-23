from datetime import datetime
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
# from django.contrib.auth.models import AbstractUser

class Comment(object):
    def __init__(self,email,content,created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

comment = Comment(email='kandelshittal@gmail.com',content='Bark')


        
class Account(models.Model):
    user_id=models.IntegerField()
    account_name=models.CharField(max_length=50)
    user=models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)



LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']


'''OTP verification for user registeration'''
class OTP_Verification(models.Model):
    email = models.IntegerField(blank=False)
    isVerified = models.BooleanField(blank=False,default=False)
    counter = models.IntegerField(default=0,blank=False)

    def __str__(self):
        return str(self.email)