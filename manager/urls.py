from django.contrib import admin
from django.urls import path, include

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
]
