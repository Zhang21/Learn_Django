"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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


'''
函数path()具有四个参数，两个必须参数: route, view，两个可选参数: kwargs, name
route:   匹配URL准则(类似正则表达式)。当Django相应一个请求时，它会从urlpatterns的第一项开始，
         按顺序依次匹配表中的项，直到找到匹配的项。这些准则不会匹配GET和POST的参数或域名。
view:    当Django找到了一个匹配的准则，就会调用这个特定的视图函数，并传入一个HttpRequest对象作为第一个参数，
         被捕获的参数一关键字参数的形式传入。
kwargs:  任意关键字参数可作为一个字典传递给目标视图函数。
name:    为你的URL取名能使你在Django的任意地方唯一地引用它，尤其在模板中。
'''

urlpatterns = [
    path('admin/', admin.site.urls),
    # add include
    path('polls/', include('polls.urls'))
    # 当包括其它URL模式时你应该总是使用include(), admin.site.urls是唯一例外
]
