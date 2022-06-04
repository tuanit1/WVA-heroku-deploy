from django.urls import path
from . import views
app_name = 'managervideo'
urlpatterns = [
    path('managervideo/<str:pk>/<int:cat>/', views.managervideo, name='managervideo'),
    path('managervideo/add/<str:pk>/<int:cat>/', views.addTv, name='addvideo'),
    path('managervideo/edit/<str:pk>/<int:cat>/<str:id>/', views.editTv, name='editvideo'),
    path('managervideo/disable/<str:pk>/<int:cat>/<str:id>/', views.disableVideo, name='disablevideo'),
]