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
from .serializer import ChangePasswordSerializer,OTPVerificationSerializer
from web_app.models import UserProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,APIView
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from .models import OTP_Verification
import base64
import string,random



'''Serializers '''

# @csrf_exempt
# def snippet_list(request):
#     if request.method=='GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetModel_Serializer(snippets,many=True)
#         return JsonResponse(serializer.data,safe=False)
    
#     elif request.method == 'POST':
#         data = JsonResponse.parse(request)
#         serializer = SnippetModel_Serializer(data=data)
#         if serializer.is_valid():
#             serializer.view()
#             return JsonResponse(serializer.data,status=201)
#         return JsonResponse(serializer.erros, status=400)


'''Request and Responses'''

@api_view(['GET','POST'])
def snippet_list(request):
    if request.method=='POST':
        snippets= Snippet.objects.all()
        serializer = SnippetModel_Serializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SnippetModel_Serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.error,status = status.HTTP_400_BAD_REQUEST)
    

'''Serializers '''
# @csrf_exempt
# def snippet_details(request,pk):
#     try:
#         snippet = Snippet.ojbects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)
    
#     if request.method=='GET':
#         serializer = SnippetModel_Serializer(snippet)
#         return JsonResponse(serializer.data)
#     elif request.method=='GET':
#         data = JsonResponse().parse(request)
#         serializer = SnippetModel_Serializer(snippet,data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.erros,status=400)
    
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)
    

'''Request and Responses'''
@api_view(['GET','PUT','PATCH'])
def snippet_detail(request,pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SnippetModel_Serializer(snippet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SnippetModel_Serializer(snippet,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''Token Based Authentication'''
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(APIView):
    def post(self,request):

        user = authenticate(username=request.data['email'],password=request.data['password'])
        # user = UserProfile.objects.filter(email=request.data('email'))
        if user:
            token,created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key,'created':created})
        else:
            return Response({'error':'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)


'''Registration Using Serializer'''
class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('phone_number')
            otp = Generate_OTP.generate_otp()
            OTP_Verification.objects.create(email=email,otp=otp)
            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def generate_otp(self, phone_number):
    #     otp = pyotp.random_base32()
    #     OTP_Verification.objects.create(phone_number=phone_number, otp=otp)
    #     return otp
    


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            otp_code = request.data.get('otp')
        try:
            otp_verification = OTP_Verification.objects.get(email=email)
            if otp_verification.otp == otp_code:
                # OTP is valid, create token and send it to user
                token = self.create_token(email)
                return Response({"token": token, "created": True}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except OTP_Verification.DoesNotExist:
            return Response({"message": "OTP not found"}, status=status.HTTP_400_BAD_REQUEST)

    def create_token(self, email):
        user = UserProfile.objects.get(email=email)
        token, created = Token.objects.get_or_create(user=user)

        return token.key
    

class Generate_OTP:
    @staticmethod
    def generate_otp(length=6):
        character = string.digits
        otp = " ".join(random.choice(character) for _ in range (length))
        return otp


# class generateKey:
#     @staticmethod
#     def returnValue(phone):
#         return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key "


# #post request to generate a otp code
# class getPhoneNumbeRegister(APIView):
#     @staticmethod
#     def get(request,phone):
#         try:
#             mobile = OTP_Verification.objects.get(mobile=phone)
#         except ObjectDoesNotExist:
#             OTP_Verification.objects.create(
#                 mobile=phone
#             )
#             mobile = OTP_Verification.objects.get(mobile=phone)
#         mobile.counter += 1
#         mobile.save()
#         keygen = generateKey()
#         key = base64.b32encode(keygen.returnValue(phone).encode())
#         otp = pyotp.HOTP(key)
#         print(otp.at(mobile.counter))
#         return Response({"OTP":otp.at(mobile.counter)},status=200)

#     @staticmethod
#     def post(request,phone):
#         try:
#             mobile = OTP_Verification.objects.get(mobile=phone)
#         except ObjectDoesNotExist:
#             return Response("User does not exist",status=404)
#         keygen=generateKey()
#         key = base64.b32encode(keygen.returnValue(phone).encode())
#         otp = pyotp.HOTP(key)
#         if otp.verify(request.data["otp"],mobile.counter):
#             mobile.isVerified = True
#             mobile.save()
#             return Response("You are authorized",status=200)
#         return Response("OTP is wrong",status=400)
    

# EXPIRED_TIME = 50 #SECONDS

# class getPhoneNumberRegistered_TimeBase(APIView):
#     @staticmethod
#     def get(request,phone):
#         try:
#             mobile = OTP_Verification.objects.get(mobile=phone)
#         except ObjectDoesNotExist:
#             return Response("User does not exist",status=400)
#         keygen = generateKey()
#         otp = base64.b16encode(keygen.returnValue(phone).encode)
#         if otp.verify(request.data["otp"]):
#             mobile.isVerified = True
#             mobile.svae()
#             return Response("You are authorized",status=200)
#         return Response("OTP is wrong/expired")