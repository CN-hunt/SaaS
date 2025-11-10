import time
import datetime
import collections
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count # ORM统计函数

from web import models


def dashboard(request, project_id):
    # 问题数据处理
    status_dict = collections.OrderedDict()  # 避免无序字典的问题
    for key, text in models.Issues.status_choices:
        status_dict[key] = {'text': text, 'count': 0}

    # 根据status分组，然后annotate里面写聚合条件，根据id计算他的数量，并赋值给ct
    issues_data = models.Issues.objects.filter(project_id=project_id).values('status').annotate(ct=Count('id'))
    for item in issues_data:
        status_dict[item['status']]['count'] = item['ct']

    # 项目成员
    user_list = models.ProjectUser.objects.filter(project_id=project_id).values('user_id', 'user__username')

    # 最近的10个问题
    top_ten = models.Issues.objects.filter(project_id=project_id, assign__isnull=False).order_by('-id')[0:10]

    context = {
        'status_dict': status_dict,
        'user_list': user_list,
        'top_ten_object': top_ten
    }
    return render(request, 'dashboard.html', context)


def issues_chart(request, project_id):
    """概览界面的图表数据"""
    today = datetime.datetime.now().date()
    date_dict = collections.OrderedDict()
    for i in range(0, 30):
        date = today - datetime.timedelta(days=i)
        date_dict[date.strftime("%Y-%m-%d")] = [time.mktime(date.timetuple()) * 1000, 0]

    # select xxxx,1 as ctime from xxxx
    # select id,name,email from table;
    # select id,name, strftime("%Y-%m-%d",create_datetime) as ctime from table;
    # "DATE_FORMAT(web_transaction.create_datetime,'%%Y-%%m-%%d')"
    result = models.Issues.objects.filter(project_id=project_id,
                                          create_datetime__gte=today - datetime.timedelta(days=30)).extra(
        select={'ctime': "strftime('%%Y-%%m-%%d',web_issues.create_datetime)"}).values('ctime').annotate(ct=Count('id'))

    for item in result:
        date_dict[item['ctime']][1] = item['ct']

    return JsonResponse({'status': True, 'data': list(date_dict.values())})