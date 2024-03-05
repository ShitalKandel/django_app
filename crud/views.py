
from rest_framework.response import Response
from rest_framework.views import APIView
from crud.models import Article,Author,Student
from crud.serializers import ArticleSerializer,AuthorSerializer,StudentSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse


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

    def perform_create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        super().perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.validated_data)

def StudentDetailView(request):
    stud = Student.objects.get(id=1)
    serializer = StudentSerializer(stud)
    json_data = JSONRenderer.render(serializer.data)
    return HttpResponse(json_data)