from django import forms 
from .models import Business

class BussForm(forms.ModelForm):
    bus_tax_cert = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn.btn-info'}))
    class Meta:
        model = Business
        fields = ['bus_name', 'bus_tax_cert','is_approved',]