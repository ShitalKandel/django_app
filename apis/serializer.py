from rest_framework import serializers
from .models import Account
from apis.models import Snippet, LANGUAGE_CHOICES,STYLE_CHOICES
from web_app.models import UserProfile
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import OTP_Verification





#serializer
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()


#modelserializer
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account 
        fields = ['user_id','account_name','user','created']


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False,allow_blank=True,max_length=100)
    code = serializers.CharField(style={'base_template':'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES ,default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES,default='friendly')

    def create(self,validated_date):
        '''another instance of snippet, validate data'''
        return Snippet.objects.create(**validated_date)
    
    def update(self,instance,validated_date):
        '''update and return an existing snippet instance , validate data '''
        instance.title=validated_date.get('title',instance.title)
        instance.code = validated_date.get('code',instance.code)
        instance.linenos = validated_date.get('linenos',instance.linenos)
        instance.style = validated_date.get()
        instance.save()
        return instance
    


'''Model Serializer'''
class SnippetModel_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields= ['id','title','code','linenos','language','style']



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = UserProfile
        fields = ['username','email','password']
        
UserProfile = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=UserProfile.objects.all())]
    # )
    # password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    otp = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'password2','otp')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password fields didn't match.")
        # otp = attrs.get('otp')
        email = attrs.get('email')
        # if not self.validate_otp(email,otp):
        #     raise serializers.ValidationError("Invalid OTP.")
        return attrs
    

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already registered.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        user = UserProfile.objects.create_user(
            email=email,
            password=password,
        )
        return user
    
    def get_otp(self):
        otp = OTP_Verification.otp
        return otp
    
    def validate_otp(self,email,otp):
        try:
            otp_validate = OTP_Verification.objects.get(email=email)
            if otp_validate.isVerified or otp_validate.counter > 3:
                raise serializers.ValidationError("OTP has already been used or expired")
            if otp_validate.otp != otp:
                raise serializers.ValidationError("Invalid OTP.")
            otp_validate.isVerified=True
            otp_validate.save()

            return True
        except OTP_Verification.DoesNotExist:
            raise serializers.ValidationError("No OTP found for this email.")


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("The old password is incorrect.")
        return value

    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("New password must be different from the old password.")
        return data
                
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, min_length=6, required=True)
                


