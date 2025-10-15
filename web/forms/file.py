from django import forms
from web import models


class FolderModelForm(forms.ModelForm):
    class Meta:
        model = models.FileRepository
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
