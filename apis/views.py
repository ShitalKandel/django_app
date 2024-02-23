from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apis.models import Snippet
from apis.serializer import SnippetModel_Serializer,UserSerializer, RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializer import RegistrationSerializer
from rest_framework import  status
from rest_framework import permissions 
from .serializer import ChangePasswordSerializer
from web_app.models import UserProfile
from rest_framework.permissions import IsAuthenticated






@csrf_exempt
def snippet_list(request):
    if request.method=='GET':
        snippets = Snippet.objects.all()
        serializer = SnippetModel_Serializer(snippets,many=True)
        return JsonResponse(serializer.data,safe=False)
    
    elif request.method == 'POST':
        data = JsonResponse.parse(request)
        serializer = SnippetModel_Serializer(data=data)
        if serializer.is_valid():
            serializer.view()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.erros, status=400)


@csrf_exempt
def snippet_details(request,pk):
    try:
        snippet = Snippet.ojbects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method=='GET':
        serializer = SnippetModel_Serializer(snippet)
        return JsonResponse(serializer.data)
    elif request.method=='GET':
        data = JsonResponse().parse(request)
        serializer = SnippetModel_Serializer(snippet,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.erros,status=400)
    
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
    



'''Token Based Authentication'''
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]




class UserLoginView(APIView):
    def post(self,request):

        user = authenticate(username=request.data['email'],password=request.data['password'])
        # user = UserProfile.objects.filter(email=request.data('email'))
        if user:
            token,created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key,'created':created})
        else:
            return Response({'error':'Invalid credentials'},status=401)


'''Registration Using Serializer'''
class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   