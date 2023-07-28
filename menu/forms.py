from django import forms
from .models import Category, menuItem
from accounts.validators import allow_only_images_validation

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =['category_name','description']

class menuItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validation])
    class Meta:
        model = menuItem
        fields =['category','menu_title','description', 'price', 'image', 'is_available']