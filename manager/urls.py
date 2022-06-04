from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('report/', include('report.urls')),
    path('category/', include('category.urls')),
    path('', include('managervideo.urls')),
    path('setting/', include('settingweb.urls')),
    path('comment/', include('comment.urls')),
    path('video/', include('videoapp.urls')),
    path('notification/', include('notification.urls')),
    # url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
