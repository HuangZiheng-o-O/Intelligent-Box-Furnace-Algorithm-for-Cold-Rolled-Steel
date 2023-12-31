from django.urls import path
# from django.conf.urls import url
from . import views
from . import Bp

urlpatterns = [
    path("", view=views.home, name="home"),
    # path("api/anneal", view=views.anneal, name="anneal"),
    # url(r'testLink', Bp.testLink),
    # url(r'bpDeep', Bp.bpDeep),
]