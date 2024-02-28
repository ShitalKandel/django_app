
from rest_framework.response import Response
from rest_framework.views import APIView
from crud.models import Article,Author
from crud.serializers import ArticleSerializer,AuthorSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication


class AuthorView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ArticleViewSets(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(request,serializer.data,headers=headers)
            

        
    def retrieve(self, request, pk=None):
        article_instance = get_object_or_404(self.queryset, pk=pk)
        serializer = ArticleSerializer(article_instance)
        return Response(serializer.data)

    def update(self, request,**kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        author_data = request.data.get('author')
        author_serializer = AuthorSerializer(data=author_data)
        if author_serializer.is_valid():
            author_instance, created = Author.objects.get_or_create(**author_serializer.validated_data)
            serializer.save(author=author_instance)
            return Response(serializer.data)
        else:
            return Response({"error": "Invalid author data"}, status=status.HTTP_400_BAD_REQUEST)
