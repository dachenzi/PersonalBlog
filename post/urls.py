from django.conf.urls import url
from post import views

urlpatterns = [

    url(r'^pub', views.pub),
    url(r'^(\d+)$', views.get),
    url(r'^$', views.getall),
]
