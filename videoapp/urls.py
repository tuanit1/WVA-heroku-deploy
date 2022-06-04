from django.urls import path
from . import views

app_name = "videoapp"

urlpatterns = [
    path('detail/<str:id>/', views.updateVideo, name='update'),
    path('create/', views.createVideo, name='create'),
    path('player/', views.videoPlayer, name='player'),
]