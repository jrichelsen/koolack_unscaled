from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Kool

class RegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.RegexField(
        label='Username', 
        max_length=30, 
        regex=r'^\w+$',
        help_text='Required. 30 characters or fewer. Letters, digits, and _ only.',
        error_message='This value must contain only letters, numbers, and underscores.')

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class KoolForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(KoolForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

    class Meta:
        model = Kool
        fields = ['content', 'image']
