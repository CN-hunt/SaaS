from django.shortcuts import render
from web.forms.file import FolderModelForm
from django.http import HttpResponse, JsonResponse
from web import models


def file(request, project_id):
    parent_object = None
    folder_id = request.GET.get('folder', '')
    if folder_id.isdecimal():
        parent_object = models.FileRepository.objects.filter(id=int(folder_id), file_type=2,
                                                             project=request.tracer.project).first()
    # 界面查看
    if request.method == 'GET':

        # 导航条
        breadcrumb_list = []
        parent = parent_object
        while parent:
            breadcrumb_list.insert(0, {'id': parent.id, 'name': parent.name})
            parent = parent.parent

        # 找到目录下所有的文件和文件及返回给前端
        queryset = models.FileRepository.objects.filter(project_id=request.tracer.project)
        if parent_object:
            # 有父级目录证明进入了某个目录
            file_object_list = queryset.filter(parent=parent_object).order_by('-file_type')
        else:
            # 代表在根目录
            file_object_list = queryset.filter(parent__isnull=True).order_by('-file_type')

        form = FolderModelForm()
        context = {'form': form,
                   'file_object_list': file_object_list,
                   'breadcrumb_list': breadcrumb_list,
                   }
        return render(request, 'file.html', context)
    form = FolderModelForm(request.POST)

    if form.is_valid():
        # 文件夹添加
        form.instance.project = request.tracer.project
        form.instance.file_type = 2
        form.instance.update_user = request.tracer.user
        form.instance.parent = parent_object
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})
