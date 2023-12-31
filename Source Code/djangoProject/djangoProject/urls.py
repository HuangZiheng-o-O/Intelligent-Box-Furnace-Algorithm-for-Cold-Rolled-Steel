"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import view  s
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf1
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from anneal import views
from anneal import Bp
from django.urls import path, include
# from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_material/', views.get_material),
    path('receive/', views.receive),
    path('bpDeep/', Bp.bpDeep),
    #path('anneal/', include('anneal.urls')),
]
