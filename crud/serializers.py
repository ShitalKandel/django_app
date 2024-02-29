from rest_framework import serializers
from crud.models import Author,Article

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


    # author = serializers.IntegerField()
    # title = serializers.CharField()
    # description = serializers.CharField()
    # body = serializers.CharField()
    # author_key = AuthorSerializer()


    def create(self, validated_data):
        author_data = validated_data.pop('author_key')
        author = Author.objects.get(id = author_data.id)
        article = Article.objects.create(author=author,**validated_data)
        return article
    
