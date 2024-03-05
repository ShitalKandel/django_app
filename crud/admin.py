from django.contrib import admin
from crud.models import Author,Article,Student

# Register your models here.
admin.site.register(Author)
admin.site.register(Article)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','name','city','roll']

