from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    username = forms.RegexField(
        label='Username', 
        max_length=30, 
        regex=r'^\w+$',
        help_text='Required. 30 characters or fewer. Letters, digits, and _ only.',
        error_message='This value must contain only letters, numbers, and underscores.')

