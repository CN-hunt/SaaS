from django.shortcuts import render, redirect
import time
from web import models
from web.forms.project import ProjectModelForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
from web.models import Project


@csrf_exempt
def project_list(request):
    """项目列表"""
    if request.method == 'GET':
        # 以下为星标及项目展示处理
        project_dict = {'star': [], 'my': [], 'join': []}
        my_project_list = models.Project.objects.filter(creator=request.tracer.user)
        for row in my_project_list:
            if row.start:
                project_dict['star'].append({"value": row, 'type': 'my'})
            else:
                project_dict['my'].append(row)

        join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)
        for item in join_project_list:
            if item.start:
                project_dict['star'].append({"value": item.project, 'type': 'join'})
            else:
                project_dict['join'].append(item.project)
        # 以上为星标及项目展示处理
        form = ProjectModelForm(request)
        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict})
    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        # 还需要在项目创建时创建一个项目腾讯COS桶
        from utils.cos import create_bucket
        name = form.cleaned_data['name']
        random_id = uuid.uuid4().hex[:8]
        bucket = name+random_id + "-1381991211"
        region = 'ap-guangzhou'
        create_bucket(bucket=bucket, region=region)
        form.instance.bucket = bucket
        form.instance.region = region
        form.instance.creator = request.tracer.user  # 以当前的登录用户为创建者,这个不写数据库将无法保存，也不报错。
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):
    """星标项目"""
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(start=True)
        return redirect('project_list')

    if project_type == 'join':
        models.Project.objects.filter(project_id=project_id, user=request.tracer.user).update(start=True)
        return redirect('project_list')
    return HttpResponse("请求错误")


def project_unstar(request, project_type, project_id):
    """取消星标"""
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(start=False)
        return redirect('project_list')

    if project_type == 'join':
        models.Project.objects.filter(project_id=project_id, user=request.tracer.user).update(start=False)
        return redirect('project_list')
    return HttpResponse("请求错误")
