from rest_framework import serializers
from snippets.models import Snippet,LANGUAGE_CHOICES,STYLE_CHOICES
from django.contrib.auth.models import User

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owners = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-hightlight',format='html')
    class Meta:
        model = Snippet
        fields = ['url','highlight','id','title','code','linenos','language','style','owners']
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True,queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['url','id','username','snippets']