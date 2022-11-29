from django import forms
from product.models import Profile

class profile_edit_form(forms.ModelForm):
    user = forms.CharField()
    email = forms.EmailField()
    phone = forms.DecimalField()
    description = forms.CharField()
    class Meta:
        model = Profile
        fields= ['user', 'email', 'phone', 'description'] 

