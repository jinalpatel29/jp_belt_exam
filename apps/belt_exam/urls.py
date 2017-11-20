from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^friends$', views.success),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add$', views.addFriend),
    url(r'^user/(?P<id>\d+)$', views.viewProfile),
     url(r'^user/(?P<id>\d+)/remove$', views.removeFriend),
]