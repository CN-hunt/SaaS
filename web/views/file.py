from django.shortcuts import render
from web.forms.file import FolderModelForm
from django.http import HttpResponse, JsonResponse
from web import models


def file(request, project_id):
    if request.method == 'GET':
        form = FolderModelForm()
        return render(request, 'file.html', {'form': form})
    form = FolderModelForm(request.POST)

    parent_object = None
    folder_id = request.GET.get('folder', '')
    if folder_id.isdecimal():
        parent_object = models.FileRepository.objects.filter(id=int(folder_id), file_type=2,
                                                             project=request.tracer.project).first()
    if form.is_valid():
        # 文件夹添加
        form.instance.project = request.tracer.project
        form.instance.file_type = 2
        form.instance.update_user = request.tracer.user
        form.instance.parent = parent_object
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})
