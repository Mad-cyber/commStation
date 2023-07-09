from django import forms 
from .models import Business

class BussForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['bus_name', 'is_approved',]