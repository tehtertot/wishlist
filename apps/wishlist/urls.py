from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^addItem$', views.addItem, name="addItem"),
    url(r'^show/(?P<id>\d*)$', views.show, name="show"),
    url(r'^addToList/(?P<id>\d*)$', views.addToList, name="addToList"),
    url(r'^remove/(?P<id>\d*)$', views.remove, name="remove"),
    url(r'^destroy/(?P<id>\d*)$', views.destroy, name="destroy")

]
