from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager


# Create your models here.


class CustomerAccountManager(BaseUserManager):
    def create_user(self,name,email,mobile,password=None):
        if not email:
            raise ValueError("User must have an email")
        if not mobile:
            raise ValueError("User should have a mobile number")
        email=self.normalize_email(email)
        user=self.model(email=email, name=name, mobile=mobile)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,name,email,mobile,password):
        user=self.create_user(email=email,name=name,mobile=mobile,password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True      
        user.save()       
        return user

class Customer(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)
    mobile=models.CharField(max_length=10)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_block=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    objects=CustomerAccountManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name','mobile']

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name
    
    def __str__(self):
        return self.email
    

    

