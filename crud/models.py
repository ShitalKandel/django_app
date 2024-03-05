from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()


class Article(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey('Author', related_name='articles',on_delete = models.CASCADE,null=True,blank=True)


    def __str__(self):
        return self.title
    

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField()
    city = models.CharField(max_length=100)

    