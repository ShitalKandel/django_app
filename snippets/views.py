from django.shortcuts import render
from snippets.serializers import UserSerializer
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action


class SnippetViewSets(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self,serializer):
        serializer.data(owner=self.request.user)   

    @action(detail=True,renderer_classes=[renderers.StaticHTMLRenderer])
    def get(self,request,*args,**kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class UserViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request,format=None):
    return Response({
        'users':reverse('user-list',request=request,format=format),
        'snippets':reverse('snippet-list',request=request,format=format)
    })