from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from  useraccount.utils import Util



class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'}, write_only=True) 
    class Meta:
        model=User
        fields=['email','name','password','password2','tc']
        extra_kwargs={'password':{'write_only':True}}
        
    #Validating password and confirm password for registration
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("The given passwords doesn't match")
        return attrs
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ['email','password']
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']
        
        
class UserChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True) 
    password2=serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']
        
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("The given passwords doesn't match")
        user.set_password(password)
        user.save()
        return attrs
    
class ForgotPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255) 
    class Meta:
        fields = ['email']
        
    def validate(self,attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            print("Encoded User_id",user_id)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token',token)
            link = 'http://localhost:3000/api/user/reset/'+user_id+'/'+token
            print('password reset link',link)
            #email link 
            body='Click Following Link to Reset the Password'+link
            data={
                'subject':'Reset your password',
                'body':body,
                'to_email':user.email    
            }
            Util.send_email(data)
            return attrs            
        else:
            raise ValidationErr('The email provided is not registered')
        
        
class ResetPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True) 
    password2=serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']
        
    def validate(self,attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            user_id = self.context.get('user_id')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("The given passwords doesn't match")
            id = smart_str(urlsafe_base64_decode(user_id))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is not valid or expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError("Token is not valid")
        
            

        
        
        
    

        
        

        

    
    
    
        
        
        

