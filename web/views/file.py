import json
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import StreamingHttpResponse, FileResponse
import requests
from utils.cos import delete_file, delete_file_list, credential

from web.forms.file import FolderModelForm
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

    fid = request.POST.get('fid', '')  # 获取前端编辑时传过来的fid
    editor_object = None
    if fid.isdecimal():
        # 文件修改
        editor_object = models.FileRepository.objects.filter(id=int(fid), file_type=2,
                                                             project=request.tracer.project).first()
    if editor_object:
        form = FolderModelForm(data=request.POST, instance=editor_object)
    else:
        form = FolderModelForm(data=request.POST)

    if form.is_valid():
        # 文件夹添加
        form.instance.project = request.tracer.project
        form.instance.file_type = 2
        form.instance.update_user = request.tracer.user
        form.instance.parent = parent_object
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def file_delete(request, project_id):
    """删除文件"""
    fid = request.GET.get('fid', '')
    delete_object = models.FileRepository.objects.filter(id=fid, project=request.tracer.project).first()
    if delete_object.file_type == 1:
        # 文件删除，腾讯cos也要删除，项目空间还回去
        request.tracer.project.use_space -= delete_object.file_size
        request.tracer.project.save()
        # cos删除文文件
        delete_file(request.tracer.project.bucket, request.tracer.project.region, delete_object.key)
        # 数据库删除
        delete_object.delete()
        return JsonResponse({'status': True})

    total_size = 0
    folder_list = [delete_object, ]
    key_list = []
    for folder in folder_list:
        child_list = models.FileRepository.objects.filter(project=request.tracer.project, parent=folder).order_by(
            '-file_type')
        for child in child_list:
            if child.file_type == 2:
                folder_list.append(child)
            else:
                total_size += child.file_size
                key_list.append({'Key': child.key})

    # cos批量删除文件
    if key_list:
        delete_file_list(request.tracer.project.bucket, request.tracer.project.region, key_list)

    # 归还容量
    if total_size:
        request.tracer.project.use_space -= total_size
        request.tracer.project.save()
    # 数据库文件的删除
    delete_object.delete()
    return JsonResponse({'status': True})


@csrf_exempt
def cos_credentials(request, project_id):
    # 获取需要上传的文件和文件大小
    per_file_limit = request.tracer.price_policy.per_file_size * 1024 * 1024
    total_file_limit = request.tracer.price_policy.project_space * 1024 * 1024 * 1024

    total_size = 0
    file_list = json.loads(request.body.decode('utf-8'))
    for item in file_list:
        if item['size'] > per_file_limit:
            msg = '文件超出大小(最大{}M)，文件{}'.format(request.tracer.price_policy.per_file_size, item['name'])
            return JsonResponse({'status': False, 'error': '文件超出大小'})
        total_size += item['size']

    # 总容量的限制
    #request.tracer.price_policy.project_space  # 允许空间
    #request.tracer.project.use_space  # 已使用空间
    if request.tracer.project.use_space + total_size > total_file_limit:
        return JsonResponse({'status': False, 'error': '超出容量请升级套餐'})

    """获取cos上传时的临时凭证"""
    data_dict = credential(request.tracer.project.bucket, request.tracer.project.region)
    return JsonResponse({'status': True, 'data': data_dict})


def file_post(request, project_id):
    """将上传成功的文件写入数据库"""
    pass
