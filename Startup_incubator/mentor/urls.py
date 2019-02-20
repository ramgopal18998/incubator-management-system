from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^update$', views.update, name='update'),
 	url(r'^assigned_startups$', views.assigned_startups, name='assigned_startups'),
    url(r'^share_videos$', views.share_videos, name='share_videos'),
    url(r'^startup_review/(?P<pk>[0-9]+)$',views.startup_review,name='startup_review'),
    url(r'^invoice$',views.compute, name='invoice'),

    
]

