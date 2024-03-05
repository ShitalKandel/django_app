from rest_framework import serializers
from crud.models import Author,Article,Student


<<<<<<< HEAD
=======

>>>>>>> parent of 1e5195cf (modelviewset (replaced, self with super to work perform_create))

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
        author,created = Author.objects.create(**author_data)
        article = Article.objects.create(author=author,**validated_data)
        return article
    
class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    roll = serializers.IntegerField()
    city = serializers.CharField(max_length=100)
