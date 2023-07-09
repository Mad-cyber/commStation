from django.db import models
from accounts.models import User, userProfile

# Create your models here.
class Business(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(userProfile, related_name='user_profile', on_delete=models.CASCADE)
    bus_name = models.CharField(max_length=100)
    bus_address = models.CharField(max_length=200)
    is_approved = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus_name

    
