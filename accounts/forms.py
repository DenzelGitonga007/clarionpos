from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Store
# Authentication
from django.contrib.auth import authenticate

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    store = forms.ModelChoiceField(queryset=Store.objects.all())
    full_name = forms.CharField()
    phone_number = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'store', 'email', 'full_name', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user

class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(required=True)
    store = forms.ModelChoiceField(queryset=Store.objects.all())
    full_name = forms.CharField()
    phone_number = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'store', 'email', 'full_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user


# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
       
        user = authenticate(username=username, password=password)
        if not user:
            self.add_error('', 'Invalid username or password')
            raise forms.ValidationError('Please check the credentials you provided')
        return cleaned_data

