from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager



# Custom User Manager
class UserAccountManager(BaseUserManager):
    def create_user(self,email,name,tc,password=None,password2=None):
        if not email:
            raise ValueError("User must have an email")
        if not name:
            raise ValueError("User should provide the name")
        email=self.normalize_email(email)
        user=self.model(email=email, name=name, tc=tc,)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,name,tc,password=None):
        user=self.create_user(email=email,name=name,tc=tc,password=password)
        user.is_admin = True
        user.is_phone_verified = True
        user.is_active = True
        user.is_gold = True
        user.is_platinum = True      
        user.save(using=self._db)       
        return user
    
    
# Models for User
class User(AbstractBaseUser):
    email=models.EmailField(verbose_name='Email',max_length=100,unique=True)
    name = models.CharField(max_length=100)
    tc=models.BooleanField()
    is_active=models.BooleanField(default=True)
    is_phone_verified=models.BooleanField(default=False)
    is_block=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_gold=models.BooleanField(default=False)
    is_platinum=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    objects=UserAccountManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name','tc']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    
    

    

