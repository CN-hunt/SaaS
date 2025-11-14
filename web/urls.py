from django.contrib import admin
from django.urls import path, include
from web.views import account, home, project, manage,wiki,file,setting,issuse,dashboard,statistics

from app01 import views

urlpatterns = [
    # 注册
    path('register/', account.register, name='register'),
    path('send/email/', account.send_email, name='send_email'),

    # 登录
    path('login/', account.login, name='login'),
    path('image/code/', account.image_code, name='image_code'),
    path('logout', account.logout, name='logout'),

    # 主页
    path('index/', home.index, name='index'),

    # 充值界面
    path('prices/',home.prices,name='prices'),
    path('payment/<int:policy_id>/',home.payment,name='payment'),
    path('pay/',home.pay,name='pay'),
    path('pay/notify/',home.pay_notify,name='pay_notify'),

    # 项目列表
    path('project/list/', project.project_list, name='project_list'),

    path('project/star/<str:project_type>/<int:project_id>/', project.project_star, name='project_star'),
    path('project/unstar/<str:project_type>/<int:project_id>/', project.project_unstar, name='project_unstar'),

    # 项目管理
    path('manage/<int:project_id>/', include([
        # path('file/', manage.file, name='file'),

        path('wiki/', wiki.wiki, name='wiki'),
        path('wiki/add/', wiki.wiki_add, name='wiki_add'),
        path('wiki/catalog/', wiki.wiki_catalog, name='wiki_catalog'),
        path('wiki/delete/<int:wiki_id>/', wiki.wiki_delete, name='wiki_delete'),
        path('wiki/edit/<int:wiki_id>/', wiki.wiki_edit, name='wiki_edit'),
        path('wiki/upload/', wiki.wiki_upload, name='wiki_upload'),  # 文件上传
        # path('wiki/detail/', wiki.wiki_detail, name='wiki_detail'),

        path('file/',file.file, name='file'),  # 文件操作
        path('file/delete/',file.file_delete, name='file_delete'),  # 删除文件夹
        path('cos/credentials/',file.cos_credentials, name='cos_credentials'),
        path('file/post/', file.file_post, name='file_post'),  # 将上传至腾讯cos的文件写入数据库
        path('file/download/<int:file_id>/', file.file_download, name='file_download'),  # 文件下载


        path('setting/', setting.setting, name='setting'),
        path('setting/delete/', setting.delete, name='setting_delete'),

        # 以下为问题列表
        path('issues/', issuse.issues, name='issues'),
        path('issues/detail/<int:issues_id>/', issuse.issues_detail, name='issues_detail'),
        path('issues/issues_record/<int:issues_id>/', issuse.issues_record, name='issues_record'),
        path('issues/change/<int:issues_id>/', issuse.issues_change, name='issues_change'),
        path('issues/invite/url/', issuse.invite_url, name='invite_url'),

        # 以下为概览操作
        path('dashboard/', dashboard.dashboard, name='dashboard'),
        path('dashboard/issues/chart', dashboard.issues_chart, name='issues_chart'),

        # 以下为统计界面
        path('statistics/', statistics.statistics, name='statistics'),
        path('statistics/statistics_priority', statistics.statistics_priority, name='statistics_priority'),
        path('statistics/statistics_project_user', statistics.statistics_project_user, name='statistics_project_user'),



    ], )),
    path('invite/join/<str:code>/',issuse.invite_join, name='invite_join'),


]
