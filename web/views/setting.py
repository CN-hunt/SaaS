from django.shortcuts import render, HttpResponse,redirect
from utils.cos import delete_bucket
from web import models

def setting(request, project_id):
    return render(request, 'setting.html')


def delete(request, project_id):
    """项目删除"""
    if request.method == 'GET':
        return render(request, 'setting_delete.html')
    project_name = request.POST.get('project_name')
    if not project_name or project_name != request.tracer.project.name:
        return render(request, 'setting_delete.html', {'error': '项目名称错误'})

    # 项目名正确则删除（仅创建者可删除）
    if request.tracer.user != request.tracer.project.creator:
        return render(request, 'setting_delete.html', {'error': '仅项目创建者才可以删除'})

    # 删除桶
    #  -必须先删除所有文件
    #  -再删除桶
    delete_bucket(request.tracer.project.bucket,request.tracer.project.bucket)
    models.Project.objects.filter(id=request.tracer.project.id).delete()


    # 删除项目
    # 返回项目主页
    return redirect('project_list')