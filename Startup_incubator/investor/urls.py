from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^show_startups$', views.show_startups, name='show_startups'),
    url(r'^update$', views.update, name='update'),
    url(r'^show_connections$', views.show_connections, name='show_connections'),
    url(r'^show_pending_connections$', views.show_pending_connections, name='show_pending_connections'),
    url(r'^accept_connection/(?P<pk>[0-9]+)$',views.accept_connection,name='accept_connection'),
	url(r'^reject_connection/(?P<pk>[0-9]+)$',views.reject_connection,name='reject_connection'),


]