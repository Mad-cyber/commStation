from django import forms 
from .models import User, userProfile
from .validators import allow_only_images_validation

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_Number', 'username', 'password']
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean ()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match, please check and try again'
            )
        

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing here', 'required':'required' }))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn.btn-info'}), validators=[allow_only_images_validation])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn.btn-info'}), validators=[allow_only_images_validation])
    class Meta:
        model = userProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'city', 'post_code', 'country','latitude','longitude']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_Number']
        
