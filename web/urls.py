from django.contrib import admin
from django.urls import path, include
from web.views import account, home, project, manage,wiki,file,setting

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

    # 项目列表
    path('project/list/', project.project_list, name='project_list'),

    path('project/star/<str:project_type>/<int:project_id>/', project.project_star, name='project_star'),
    path('project/unstar/<str:project_type>/<int:project_id>/', project.project_unstar, name='project_unstar'),

    # 项目管理
    path('manage/<int:project_id>/', include([
        path('dashboard/', manage.dashboard, name='dashboard'),
        path('issues/', manage.issues, name='issues'),
        path('statistics/', manage.statistics, name='statistics'),
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
    ], )),

]
