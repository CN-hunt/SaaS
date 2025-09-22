from web import models
from django import forms


class WikiModelForm(forms.ModelForm):
    class Meta:
        model = models.Wiki
        exclude = ['project', ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 找到想要的字段把它绑定的数据重置,不然别的项目也会展示当前项目的文章
        # 数据 = 去数据库中获取当前项目所有的wiki标题
        total_data_list = [('','请选择'),]  # 创建一个默认不需要父级文章的选项
        data_list = models.Wiki.objects.filter(project=request.tracer.project).values_list('id', 'title')
        total_data_list.extend(data_list)

        # self.fields['parent'].choices = [(1, 'dd'), (2, 'cc')]  # 重写choice
        self.fields['parent'].choices = total_data_list
