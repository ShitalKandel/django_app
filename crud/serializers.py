from rest_framework import serializers
from crud.models import Author,Article,Student

from django.db.models.query import QuerySet

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name','email']


class ArticleSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),source='author_key')

    class Meta:
        model = Article
        fields = ['title','description','body','author']



    def create(self, validated_data):
        author_data = validated_data.pop('author_key')
        author = Author.objects.get(id = author_data.id)
        article = Article.objects.create(author=author,**validated_data)
        return article
    
class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    roll = serializers.IntegerField()
    city = serializers.CharField(max_length=100)
