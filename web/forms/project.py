from django import forms
from web import models
from web.models import Project
from django.core.exceptions import ValidationError
from web.forms.widgets import ColorRadioSelect  # 自己重写的样式


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'color': ColorRadioSelect(attrs={'class': 'color-radio'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_name(self):
        """项目校验"""
        name = self.cleaned_data['name']
        # 当前用户是否已经创建过此项目
        exists = models.Project.objects.filter(name=name, creator=self.request.tracer.user).exists()
        if exists:
            raise ValidationError("项目名已经存在")
        # 当前用户是否还有创建额度
        # 最多创建多少项目
        # self.request.tracer.price_policy.project_num

        # 当前已经创建的项目
        count = models.Project.objects.filter(creator=self.request.tracer.user).count()

        if count >= self.request.tracer.price_policy.project_num:
            raise ValidationError("项目已达上限，请升级您的套餐")

        return name
