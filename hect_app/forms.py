from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label='username',max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='password',max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label='captcha')

class RegisterForm(forms.Form):
    gender = (
        ('male','Male'),
        ('female','Female'),
    )
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="password_confirm", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='sex', choices=gender)
    captcha = CaptchaField(label='captcha')

# class ImagesForm(forms.Form):
#     title = forms.CharField(label="Select Image",max_length=128)
#     file = forms.FileField(upload_to="img")
#     username = forms.CharField(max_length=128)
