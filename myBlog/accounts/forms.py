from django import forms


from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username= forms.CharField()
    password= forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username= self.cleaned_data.get('username')
        password= self.cleaned_data.get('password')
        user= authenticate(username=username, password=password)
        if username and password:
            if not user:
                raise forms.ValidationError("This user doesn't exist")
            if not user.check_password(password):
                raise forms.ValidationError("Password is incorrect")
            if not user.is_active:
                raise forms.ValidationError("This user is not active")

        return super(UserLoginForm, self).clean(*args,**kwargs)


class UserRegistrationForm(forms.ModelForm):
    password= forms.CharField(widget=forms.PasswordInput)
    email= forms.EmailField(label='Email Address')
    first_name= forms.CharField(label='First Name')
    last_name= forms.CharField(label='Last Name')

    class Meta:
        model= User
        fields= [
            'username',
            'first_name',
            'last_name',
            'password',
            'email'
        ]

    def clean_email(self):
        email= self.cleaned_data.get('email')
        email_qs= User.objects.filter(email=email)

        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")

        return email




