from django.shortcuts import render, redirect
from web.forms.wiki import WikiModelForm
from django.urls import reverse  # 反向生成URL
from web import models
from django.http import HttpResponse, JsonResponse


def wiki(request, project_id):
    """wiki首页"""
    wiki_id = request.GET.get('wiki_id')
    if not wiki_id or not wiki_id.isdecimal():
        return render(request, 'wiki.html')
        # 文章详细
    wiki_object = models.Wiki.objects.filter(id=wiki_id, project_id=project_id).first()
    # 文章首页
    return render(request, 'wiki.html', {'wiki_object': wiki_object})


def wiki_add(request, project_id):
    """wiki添加"""
    if request.method == 'GET':
        form = WikiModelForm(request)
        return render(request, 'wiki_add.html', {'form': form})
    form = WikiModelForm(request, data=request.POST)
    if form.is_valid():

        # 判断用户是否已经选择父级文章
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1

        form.instance.project = request.tracer.project  # 自生成字段
        form.save()
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)
    return render(request, 'wiki_add.html', {'form': form})


def wiki_catalog(request, project_id):
    """wiki目录"""
    # 获取当前项目所有的wiki目录
    # data = models.Wiki.objects.filter(project=request.tracer.project).values_list('id','title','parent_id')
    data = models.Wiki.objects.filter(project=request.tracer.project).values('id', 'title', 'parent_id').order_by(
        'depth', 'id')
    return JsonResponse({'status': True, 'data': list(data)})


# def wiki_detail(request, project_id):
#     """
#     查看文章详细界面
#     /detail/?wiki_id=1
#     /detail/?wiki_id=2
#     """
#     return HttpResponse("查看详情")


def wiki_delete(request, project_id, wiki_id):
    """删除文章"""
    models.Wiki.objects.filter(project_id=project_id, id=wiki_id).delete()
    url = reverse('wiki', kwargs={'project_id': project_id})
    return redirect(url)


def wiki_edit(request, project_id, wiki_id):
    """文章编辑"""
    wiki_object = models.Wiki.objects.filter(id=wiki_id, project=request.tracer.project).first()
    if not wiki_id:
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)
    if request.method == 'GET':
        form = WikiModelForm(request, instance=wiki_object)
        return render(request, 'wiki_add.html', {'form': form})
    form = WikiModelForm(request, data=request.POST, instance=wiki_object)
    if form.is_valid():
        # 判断用户是否已经选择父级文章
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        form.save()
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)
