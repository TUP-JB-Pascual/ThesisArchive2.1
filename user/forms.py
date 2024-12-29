from typing import Any
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, SetPasswordForm
from .models import CustomUser
from django import forms
from django.utils.safestring import mark_safe


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.TextInput())
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput())
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput())
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label = 'Email:'

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['first_name'].label = 'First Name:'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['last_name'].label = 'Last Name:'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = 'Password:'
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = 'Confirm Password:'
        #self.fields['password2'].help_text = mark_safe('<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password can\'t be a commonly used password.</li><li>Your password must contain at least 8 characters.</li><li>Your password must contain at least 1 numeric character.</li><li>Your password must contain at least 1 lowercase character.</li><li>Your password must contain at least 1 uppercase character.</li><li>Your password must contain at least 1 special character.</li></ul>')
        self.fields['password2'].help_text = mark_safe('<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password can\'t be a commonly used password.</li><li>Your password must contain at least 8 characters.</li><li>Your password must contain at least 1 numeric character, 1 lowercase character, 1 uppercase character and 1 special character.</li></ul>')
    
        #self.fields['email'].widget.attrs['pattern'] = "[a-z.]*[@]\bgsfe.tupcavite.edu.ph"

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@gsfe.tupcavite.edu.ph" not in data:   # any check you need
            raise forms.ValidationError("You must use a 'gsfe.tupcavite.edu.ph address")
        return data

class UpdateProfileForm(UserChangeForm):
    # HIDE PASSWORD
    password = None
    email = forms.EmailField(label='Email:', widget=forms.TextInput())
    first_name = forms.CharField(label='First Name:', max_length=100, widget=forms.TextInput())
    middle_name = forms.CharField(label='Middle Name:', max_length=100, required=False, widget=forms.TextInput())
    last_name = forms.CharField(label='Last Name:', max_length=100, widget=forms.TextInput())
    suffix_name = forms.CharField(label='Suffix: ', max_length=50, required=False, widget=forms.TextInput())
    
    class Meta:
            model = CustomUser
            fields = ('email', 'first_name', 'middle_name', 'last_name', 'suffix_name')

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control readOnlyTextBox'
        self.fields['email'].widget.attrs['placeholder'] = ''
        self.fields['email'].widget.attrs['readonly'] = 'readonly'
        self.fields['email'].widget.attrs['tabindex'] = '-1'
        self.fields['email'].widget.attrs['id'] = 'unclickable'
        self.fields['email'].label = 'Email:'

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = ''
        self.fields['first_name'].widget.attrs['required'] = 'True'
        self.fields['first_name'].label = 'First Name:'
        
        self.fields['middle_name'].widget.attrs['class'] = 'form-control'
        self.fields['middle_name'].widget.attrs['placeholder'] = ''
        self.fields['middle_name'].label = 'Middle Name:'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = ''
        self.fields['last_name'].label = 'Last Name:'

        self.fields['suffix_name'].widget.attrs['class'] = 'form-control'
        self.fields['suffix_name'].widget.attrs['placeholder'] = ''
        self.fields['suffix_name'].label = 'Suffix:'

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = CustomUser
        fields = ['new_password1', 'new_password2']
          
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password1'].label = 'New Password: '
        self.fields['new_password1'].help_text = ''
        
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'
        self.fields['new_password2'].label = 'Confirm Password: '
        self.fields['new_password2'].help_text = mark_safe('<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password can\'t be a commonly used password.</li><li>Your password must contain at least 8 characters.</li><li>Your password must contain at least 1 numeric character, 1 lowercase character, 1 uppercase character and 1 special character.</li></ul>')
    