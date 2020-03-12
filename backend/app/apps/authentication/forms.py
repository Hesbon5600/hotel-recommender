from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

from .models import User


class UserSignupForm(forms.ModelForm):
    """
    Signup form class
    """
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email', "class": "form-control", "required":"required"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password', "class": "form-control"}
    ))
    first_name = forms.CharField(
        label=None, widget=forms.TextInput(attrs={'placeholder': 'Enter First Name',
                                                  "class": "form-control"}))
    last_name = forms.CharField(
        label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', "class": "form-control"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.add_input(Submit('submit', 'Signup'))


class UserLoginForm(AuthenticationForm):
    """
    Login Form class
    """
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email', "class": "form-control", "required":"required"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', "class": "form-control"}))

    class Meta:
        model = User
        fields = ('email', 'password',)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = 'form-login'
        self.helper.form_class = 'form-login'
        self.helper.form_method = 'POST'
        self.helper.form_action = 'login'
        self.helper.field_class = 'form-control input-lg'
        self.helper.form_show_errors = True

        self.helper.layout.append(
            Submit('login', 'Login', css_class='btn login-form__btn submit w-100'))
