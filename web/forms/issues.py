from django import forms
from web import models
from web.models import Issues


class IssueModelForm(forms.ModelForm):
    class Meta:
        model = models.Issues
        exclude = ['project', 'creator', 'create_datetime', 'latest_update_datetime', 'update_datetime']

        widgets = {
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assign': forms.Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control'}),
            'mode': forms.Select(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}),
            'attention': forms.SelectMultiple(
                attrs={'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-actions-box': 'true'}),
            # 多选下拉框
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'issues_type': forms.Select(attrs={'class': 'form-control'}),
            'module': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 获取问题类型
        self.fields['issues_type'].choices = models.IssuesType.objects.filter(
            project=request.tracer.project).values_list('id', 'title')

        # 2.获取当前项目的所有模块
        module_list = [("", "没有选中任何项"), ]
        module_object_list = models.Module.objects.filter(project=request.tracer.project).values_list('id', 'title')
        module_list.extend(module_object_list)
        self.fields['module'].choices = module_list

        # 3.指派和关注者
        # 数据库找到当前项目的参与者 和 创建者
        total_user_list = [(request.tracer.project.creator_id, request.tracer.project.creator.username), ]
        project_user_list = models.ProjectUser.objects.filter(project=request.tracer.project).values_list('user_id',
                                                                                                          'user__username')
        total_user_list.extend(project_user_list)

        self.fields['assign'].choices = [("", "没有选中任何项")] + total_user_list
        self.fields['attention'].choices = total_user_list

        # 4. 当前项目已创建的问题
        parent_list = [("", "没有选中任何项")]
        parent_object_list = models.Issues.objects.filter(project=request.tracer.project).values_list('id', 'subject')
        parent_list.extend(parent_object_list)
        self.fields['parent'].choices = parent_list
