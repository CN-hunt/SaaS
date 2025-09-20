from django.template import Library

from web import models
from web.models import Project

register = Library()


@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list(request):
    # 我创建的项目
    my_project_list = models.Project.objects.filter(creator=request.tracer.user)

    # 我参与的项目
    join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)
    return {'my': my_project_list, 'join': join_project_list}
