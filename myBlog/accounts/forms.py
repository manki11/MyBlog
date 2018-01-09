from django import forms

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

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



