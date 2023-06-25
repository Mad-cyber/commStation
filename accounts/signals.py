from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, userProfile



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