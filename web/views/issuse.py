from django.shortcuts import render
from web.forms.issues import IssueModelForm
from django.http import HttpResponse, JsonResponse
from web import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def issues(request, project_id):
    if request.method == 'GET':
        form = IssueModelForm(request)

        # 分页组件
        issues_object_list = models.Issues.objects.filter(project_id=project_id)
        paginator = Paginator(issues_object_list, 5)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        context = {'form': form, 'issues_object_list': page_obj,'page_obj': page_obj}
        return render(request, 'issues.html', context)

    print(request.POST)
    form = IssueModelForm(request, data=request.POST)
    if form.is_valid():
        # 添加问题
        form.instance.project = request.tracer.project
        form.instance.creator = request.tracer.user
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def issues_detail(request, project_id,issues_id):
    """编辑问题界面"""
    issues_object=models.Issues.objects.filter(project_id=project_id,id=issues_id).first()
    form = IssueModelForm(request,instance=issues_object)
    return render(request, 'issues_detail.html', {'form': form,})