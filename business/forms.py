from django import forms 
from .models import Business, OpenHours
from accounts.validators import allow_only_images_validation

class BussForm(forms.ModelForm):
    bus_tax_cert = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn.btn-info'}), validators=[allow_only_images_validation])
    class Meta:
        model = Business
        fields = ['bus_name', 'bus_tax_cert','is_approved',]

class OpenHoursForm(forms.ModelForm):
    class Meta:
        model = OpenHours
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']