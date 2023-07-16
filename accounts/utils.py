from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings



#utils file creating the permissions for each of the registered users, if cus then cus dashboard etc
def detectUser(user):
    if user.role == 1:
        redirectUrl = 'bussDash'
        return redirectUrl
    elif user.role ==2:
        redirectUrl = 'custDash'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
# email verifcation token and message taken from https://www.rockandnull.com/django-email-verification/
def send_verification_email(request,user):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = 'Please verify your email address'
    message = render_to_string('accounts/emails/account_verif_email.html',{
        'user': user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    #send email subject with the token
    mail = EmailMessage(mail_subject,message, from_email, to=[to_email])
    mail.send()