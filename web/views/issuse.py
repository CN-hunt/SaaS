from django.shortcuts import render
from web.forms.issues import IssueModelForm, IssuesReplyModelForm
from django.http import HttpResponse, JsonResponse
from web import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
import json


def issues(request, project_id):
    if request.method == 'GET':
        form = IssueModelForm(request)

        # 分页组件
        issues_object_list = models.Issues.objects.filter(project_id=project_id)
        paginator = Paginator(issues_object_list, 5)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        context = {'form': form, 'issues_object_list': page_obj, 'page_obj': page_obj}
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


def issues_detail(request, project_id, issues_id):
    """编辑问题界面"""
    issues_object = models.Issues.objects.filter(project_id=project_id, id=issues_id).first()
    form = IssueModelForm(request, instance=issues_object)
    return render(request, 'issues_detail.html', {'form': form, 'issues_object': issues_object})


@csrf_exempt
def issues_record(request, project_id, issues_id):
    """ 初始化操作记录 """

    # 判断是否可以评论和是否可以操作这个问题
    if request.method == "GET":
        reply_list = models.IssuesReply.objects.filter(issues_id=issues_id, issues__project=request.tracer.project)
        # 将queryset转换为json格式
        data_list = []
        for row in reply_list:
            data = {
                'id': row.id,
                'reply_type_text': row.get_reply_type_display(),
                'content': row.content,
                'creator': row.creator.username,
                'datetime': row.create_datetime.strftime("%Y-%m-%d %H:%M"),
                'parent_id': row.reply_id
            }
            data_list.append(data)

        return JsonResponse({'status': True, 'data': data_list})

    form = IssuesReplyModelForm(data=request.POST)
    if form.is_valid():
        form.instance.issues_id = issues_id
        form.instance.reply_type = 2
        form.instance.creator = request.tracer.user
        instance = form.save()
        info = {
            'id': instance.id,
            'reply_type_text': instance.get_reply_type_display(),
            'content': instance.content,
            'creator': instance.creator.username,
            'datetime': instance.create_datetime.strftime("%Y-%m-%d %H:%M"),
            'parent_id': instance.reply_id
        }

        return JsonResponse({'status': True, 'data': info})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def issues_change(request, project_id, issues_id):
    issues_object = models.Issues.objects.filter(id=issues_id, project_id=project_id).first()

    post_dict = json.loads(request.body.decode('utf-8'))

    # 取到前端返回的值
    name = post_dict.get('name')
    value = post_dict.get('value')
    field_object = models.Issues._meta.get_field(name)

    # 1. 数据库字段更新
    # 1.1 文本
    if name in ["subject", 'desc', 'start_date', 'end_date']:

        if not value:
            if not field_object.null:
                return JsonResponse({'status': False, 'error': "您选择的值不能为空"})
            setattr(issues_object, name, None)
            issues_object.save()
            change_record = "{}更新为空".format(field_object.verbose_name)
        else:
            setattr(issues_object, name, value)
            issues_object.save()
            # 记录：xx更为了value
            change_record = "{}更新为{}".format(field_object.verbose_name, value)

        new_object = models.IssuesReply.objects.create(
            reply_type=1,
            issues=issues_object,
            content=change_record,
            creator=request.tracer.user,
        )
        new_reply_dict = {  # 数据返回前端
            'id': new_object.id,
            'reply_type_text': new_object.get_reply_type_display(),
            'content': new_object.content,
            'creator': new_object.creator.username,
            'datetime': new_object.create_datetime.strftime("%Y-%m-%d %H:%M"),
            'parent_id': new_object.reply_id
        }
        return JsonResponse({'status': True, 'data': new_reply_dict})
