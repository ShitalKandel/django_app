from apis.models import SnippetModel
from apis.serializer import SnippetModel_Serializer, RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializer import RegistrationSerializer
from rest_framework import  status
from rest_framework import permissions 
from apis.serializer import ChangePasswordSerializer,ItemSerialzer,LocationSerializer,OTPVerificationSerializer
from facebook_clone.models import UserProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view,APIView
from apis.models import OTP_VerificationModel
import string,random
from django.core.mail import send_mail
from django.conf import settings 
from apis.models import ItemModel,Item_locationModel
from django.core.exceptions import ValidationError



'''Request and Responses'''

@api_view(['GET','POST'])
def snippet_list(request):
    if request.method=='POST':
        snippets= SnippetModel.objects.all()
        serializer = SnippetModel_Serializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SnippetModel_Serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.error,status = status.HTTP_400_BAD_REQUEST)
    
    

'''Request and Responses'''
@api_view(['GET','PUT','PATCH'])
def snippet_detail(request,pk):
    try:
        snippet = SnippetModel.objects.get(pk=pk)
    except SnippetModel.DoesNotExist:
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
class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginAPIView(APIView):
    def post(self,request):

        user = authenticate(username=request.data['email'],password=request.data['password'])
        if user:
            token,created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key,'created':created})
        else:
            return Response({'error':'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)


def generate_otp():
    character = string.digits
    otp = str("".join(random.choice(character) for _ in range(6)))
    return otp


'''Registration Using Serializer'''
class RegisterAPIView(APIView):
    def post(self, request):
        if request.method == 'POST':
            serializer= RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                user =serializer.save()
                otp = generate_otp()

                # otp = OTP_Verification
                OTP_VerificationModel.objects.create(user=user,otp=otp)
                return Response({"Your otp":otp,"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def send_otp(self,email,otp):
        subject = 'OTP  for validation.'
        message = f"your otp is {otp}"
        from_email = settings.EMAIL_HOST_USER
        receipt = email
        send_mail(subject,message,from_email,receipt)
        return otp

class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class VerifyOTPAPIView(APIView):
    def post(self, request, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            otp_code = request.data.get('otp')
        try:
            otp_verification = OTP_VerificationModel.objects.get(email=email)
            if otp_verification.otp == otp_code:
                # OTP is valid, create token and send it to user
                token = self.create_token(email)
                otp_code = self.generate_otp()
                return Response({"token": token,"otp":otp_code, "created": True}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except OTP_VerificationModel.DoesNotExist:
            return Response({"message": "OTP not found"}, status=status.HTTP_400_BAD_REQUEST)

    def create_token(self, email):
        user = UserProfile.objects.get(email=email)
        token, created = Token.objects.get_or_create(user=user)
        return token.key

  


class ItemListAPIView(generics.ListCreateAPIView):
    serializer_class = ItemSerialzer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        queryset = ItemModel.objects.all()
        location = self.request.query_params.get('location')
        if location is not None:
            queryset = queryset.filter(Item_location=location)
        return queryset
    


class LocationListAPIView(generics.ListCreateAPIView):
    serializer_class = LocationSerializer
    queryset = Item_locationModel.objects.all()

    

class ItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerialzer
    queryset = ItemModel.objects.all()


class LocationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LocationSerializer
    queryset = Item_locationModel.objects.all()
     
