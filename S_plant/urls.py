"""S_plant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from app01 import views # 路由分发出去了所以不再需要这个

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app01/', include('app01.urls')),  # 分发路由，以后以qpp01为前缀访问时，都将被分发至app01下的urls.py
    path('', include('web.urls'))  # 不以app01开头的都将被分发至web下的urls.py
]
