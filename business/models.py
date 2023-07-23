from django.db import models
from accounts.models import User, userProfile
from accounts.utils import send_notification
import logging

logger = logging.getLogger(__name__)

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

    # def full_address(self):
    #      return f'{self.address_line_one}, {self.address_line_two}'


    def __str__(self):
        return self.bus_name

def save(self, *args, **kwargs):
        logger.info("Saving Business object...")
        if self.pk is not None:
            # Update approval for business
            orig = Business.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/buss_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
                if self.is_approved:
                    # Send the approval email for business
                    mail_subject = "You have been Approved for Communication Station!"
                else:
                    # Send rejection email
                    mail_subject = "We regret to inform you that your application has been rejected"

                # Call the send_notification function to send the email
                send_notification(mail_subject, mail_template, context)

        return super(Business, self).save(*args, **kwargs)
    
    
# def save(self, *args, **kwargs):
#     logger.info("Saving Business object...")
#     if self.pk is not None:
#         #update approval for business
#         orig = Business.objects.get(pk=self.pk)
#         if orig.is_approved != self.is_approved:
#             mail_template = 'accounts/emails/buss_approval_email.html'
#             context = {
#                     'user': self.user,
#                     'is_approved': self.is_approved,
#                 }
#             if self.is_approved == True:
#                 #send the approval email for business
#                 mail_subject = "You have been Approved for Communcation Station!"
#                 send_notification(mail_subject, mail_template, context)
#             else:
#                 #send rejection email
#                 mail_subject = "We regret to inform you that your application has been rejected"
#                 send_notification(mail_subject, mail_template, context)
#     return super(Business, self).save(*args, **kwargs)


    
