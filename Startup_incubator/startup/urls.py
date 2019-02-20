from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^train/$',views.train, name='train'),
    url(r'^test/$',views.test, name='test'),
    url(r'^predict/$',views.get_recommendations, name='predict'),
    url(r'^about/$',views.about_us),
    url(r'^mentors/$',views.mentors),
    url(r'^investors/$',views.investors),
    url(r'^mentor_popup/(?P<pk>[0-9]+)$',views.mentor_profile_popup,name='mentor_popup'),
    url(r'^investor_popup/(?P<pk>[0-9]+)$',views.investor_profile_popup,name='investor_popup'),
    url(r'^startup_popup/(?P<pk>[0-9]+)$',views.startup_profile_popup,name='startup_popup'),
    url(r'^apply_incubation/$',views.apply_incubation),
    url(r'^apply_fund/$',views.apply_fund),

    url(r'^send_connection_request/(?P<pk>[0-9]+)$',views.send_connection_request,name='send_connection_request'),
    url(r'^show_connections$', views.show_connections, name='show_connections'),
    url(r'^show_pending_connections$', views.show_pending_connections, name='show_pending_connections'),
    url(r'^accept_connection/(?P<pk>[0-9]+)$',views.accept_connection,name='accept_connection'),
    url(r'^reject_connection/(?P<pk>[0-9]+)$',views.reject_connection,name='reject_connection'),

    url(r'^generate_ticket/$',views.generate_ticket,name='generate_ticket'),
    url(r'^select_booking/$',views.select_booking,name='select_booking'),   
    url(r'^show_bookings/$',views.show_bookings,name='show_bookings'),

    url(r'^my_videos/$',views.my_videos,name='my_videos'),
url(r'^complete_milestone/(?P<pk>[0-9]+)$',views.complete_milestone,name='complete_milestone'),
    url(r'^show_milestones/$',views.show_milestones,name='show_milestones'),
    url(r'^mentor_review/(?P<pk>[0-9]+)$',views.mentor_review,name='mentor_review'),
    url(r'^my_documents/$',views.my_documents,name='my_documents'),
    url(r'^notifications/$',views.notifications,name='notifications'),
    url(r'^see_ticket/(?P<pk>[0-9]+)$',views.see_ticket,name='see_ticket'),
    url(r'^mytickets/$',views.mytickets,name='mytickets'),
    

    
    url(r'^my_videos/$',views.my_videos,name='my_videos'),
    url(r'^my_documents/$',views.my_documents,name='my_documents'),



    url(r'^generate_ticket/$',views.generate_ticket,name='generate_ticket'),
    url(r'^upload_documents$', views.upload_documents, name='upload_documents'),

]
