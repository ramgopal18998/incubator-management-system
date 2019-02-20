
from django.conf.urls import url,include
from django.contrib import admin
from login import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^startup/',include('startup.urls',namespace='startup')),
    url(r'^investor/',include('investor.urls',namespace='investor')),
    url(r'^mentor/',include('mentor.urls',namespace='mentor')),
    url(r'^login/',include('login.urls',namespace='login')),
    url(r'^administrator/',include('administrator.urls',namespace='administrator')),
    url(r'^register/',views.register, name='register'),
    url(r'^library/',include('library.urls',namespace='library')),
    url(r'^rent/',include('rent.urls',namespace='rent'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)