from django import forms
from web import models
from utils.cos import check_file


class FolderModelForm(forms.ModelForm):
    class Meta:
        model = models.FileRepository
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FileModelForm(forms.ModelForm):
    etag = forms.CharField(label='ETag')

    class Meta:
        model = models.FileRepository
        exclude = ['project', 'file_type', 'update_user', 'update_datetime']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_file_path(self):
        return 'https://{}'.format(self.cleaned_data['file_path'])


"""
# 防止恶意请求方法
    def clean(self):
        key = self.cleaned_data['key']
        etag = self.cleaned_data['etag']
        size = self.cleaned_data['size']
        if not key or not etag:
            return self.cleaned_data
        from qcloud_cos.cos_exception import CosServiceError
        try:
            result = check_file(
                bucket=self.request.tracer.project.bucket,
                region=self.request.tracer.project.region,
                key=key,
            )
        except CosServiceError as e:
            self.add_error('key', '文件不存在')
            return self.cleaned_data

        cos_etag = result.get('etag')
        if cos_etag != etag:
            self.add_error('etag','ETage错误')

        cos_length = result.get('Content-Length')
        if int(cos_length) != size:
            self.add_error('size','文件体积错误')
            
        return self.cleaned_data
"""
