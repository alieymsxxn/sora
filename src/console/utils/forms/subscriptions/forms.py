from allauth.account.forms import LoginForm, SignupForm, ChangePasswordForm
from django import forms


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # here you can change the fields
        self.fields['login'] = forms.CharField(label='Email or Username')

class CustomSignUpForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # here you can change the fields
        self.fields['password2'] = forms.CharField(label='Confirm passowrd')

class CustomChangePasswordForm(ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # here you can change the fields
        self.fields['oldpassword'] = forms.CharField(label='Old passowrd')
        self.fields['password1'] = forms.CharField(label='New passowrd')
        self.fields['password2'] = forms.CharField(label='Confirm passowrd')
