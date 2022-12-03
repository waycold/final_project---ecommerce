from django import forms
from product.models import Profile, Comments

class profile_edit_form(forms.ModelForm):
    user = forms.CharField()
    email = forms.EmailField()
    phone = forms.DecimalField()
    description = forms.CharField()
    class Meta:
        model = Profile
        fields= ['user', 'email', 'phone', 'description'] 

class comments_form(forms.ModelForm):
    body = forms.CharField(label = '', widget = forms.Textarea(attrs={'placeholder': 'text here...', 'rows': 3, 'cols': 70}))
    requered_css_class = 'required-field'
    class Meta:
        model = Comments
        fields= ['body']
        labels = {
            'body': (''),
        }