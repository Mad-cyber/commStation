from django.db import models
from accounts.models import User, userProfile
from accounts.utils import send_notifcation

# Create your models here.
class Business(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(userProfile, related_name='user_profile', on_delete=models.CASCADE)
    bus_name = models.CharField(max_length=100)
    bus_address = models.CharField(max_length=200)
    bus_tax_cert = models.ImageField(upload_to='business/taxCert')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus_name
    
def save(self, *args, **kwargs):
    if self.pk is not None:
        #update approval for business
        orig = Business.objects.get(pk=self.pk)
        if orig.is_approved != self.is_approved:
            mail_template = 'accounts/emails/buss_approval_email.html'
            context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
            if self.is_approved == True:
                #send the approval email for business
                mail_subject = "You have been Approved for Communcation Station!"
                send_notifcation(mail_subject, mail_template,context)
            else:
                #send rejection email
                mail_subject = "We regret to infrom to inform you that you application has been rejected"
                send_notifcation(mail_subject, mail_template,context)
    return super(Business, self).save(*args, **kwargs)


    
