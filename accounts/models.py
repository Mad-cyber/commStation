from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.db.models.fields.related import OneToOneField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


# Create your models here.
#only contains methods for creating users https://docs.djangoproject.com/en/4.2/topics/db/examples/one_to_one/
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must enter an email address')
        
        if not username:
            raise ValueError('User must enter a username')
        
        user = self.model (
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Superuser must enter an email address')
        
        if not username:
            raise ValueError('Superuser must enter a username')
        
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


#this is for the super user
class User(AbstractBaseUser):
    BUSINESS = 1
    CUSTOMER = 2
    #USER = 3

    ROLE = (
        (BUSINESS, 'Business'),
        (CUSTOMER, 'Customer'),
        #(USER, 'user')

    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_Number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE, blank=True, null=True)

    #required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifed_date = models.DateTimeField(auto_now_add=True)
    #is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    #is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True
    
class userProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user/profile_pictures',  blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos',  blank=True, null=True)
    address_line_one = models.CharField(max_length=50, blank=True, null=True)
    address_line_two = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    post_code = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    staff_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
# the below is creating an error with empty email field or user field    
# @receiver(post_save, sender=User)
# def post_save_create_profile_receiver(sender, instance, created, **kwargs):
#     print(created)
#     if created:
#         userProfile.objects.create(user=instance)
#         print('user profile is created')
    

#post_save.connect(post_save_create_profile_receiver, sender=User) using singals https://docs.djangoproject.com/en/4.2/ref/signals/

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created and instance.email:
        userProfile.objects.create(user=instance)
        print('User profile created')
    else:
        try:
            profile = userProfile.objects.get(user=instance)
            profile.save
        except:
            #create a userprofile only if it doesnt exist
            print('Profile was not found')
        print('the user has been updated sucessfully')

@receiver(pre_save, sender=User)
def per_save_profile(sender, instance, **kwargs):
    print(instance.username, 'user has been saved sucessfully')