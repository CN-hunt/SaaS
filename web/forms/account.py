from django import forms
from web import models


class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': '确认密码'}))

    class Meta:
        model = models.UserInfo
        fields = '__all__'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field', 'placeholder': '用户名'}),
            'email': forms.TextInput(attrs={'class': 'input-field', 'placeholder': '邮箱', 'id': 'EM'}),
            'password': forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': '密码'}),
        }
