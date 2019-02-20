from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pay_rent$', views.pay_rent, name='pay_rent')
]