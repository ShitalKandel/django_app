from rest_framework import serializers
from crud.models import Author,Article
from rest_framework.response import Response

    
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name','email']


class ArticleSerializer(serializers.Serializer):

    # author = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    body = serializers.CharField()
    author_key = AuthorSerializer()


    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.body = validated_data.get('body', instance.body)
    #     instance.author_id = validated_data.get('author_id', instance.author_id)

    #     instance.save()
    #     return instance
    
    def validate_author(self, value):
        author = Author.objects.filter(id=value).first()
        if author:
            return value
        raise serializers.ValidationError("No author found")
