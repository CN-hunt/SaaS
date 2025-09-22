from django.shortcuts import render, redirect
from web.forms.wiki import WikiModelForm
from django.urls import reverse  # 反向生成URL
from web import models
from django.http import HttpResponse, JsonResponse


def wiki(request, project_id):
    """wiki首页"""
    return render(request, 'wiki.html')


def wiki_add(request, project_id):
    """wiki添加"""
    if request.method == 'GET':
        form = WikiModelForm(request)
        return render(request, 'wiki_add.html', {'form': form})
    form = WikiModelForm(request, data=request.POST)
    if form.is_valid():
        form.instance.project = request.tracer.project  # 自生成字段
        form.save()
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)
    return render(request, 'wiki_add.html', {'form': form})


def wiki_catalog(request, project_id):
    """wiki目录"""
    # 获取当前项目所有的wiki目录
    # data = models.Wiki.objects.filter(project=request.tracer.project).values_list('id','title','parent_id')
    data = models.Wiki.objects.filter(project=request.tracer.project).values('id', 'title', 'parent_id')
    return JsonResponse({'status': True, 'data': list(data)})
