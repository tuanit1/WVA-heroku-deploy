from django.urls import path
from . import views
app_name = 'settingweb'
urlpatterns = [
    path('setting/<str:able>/', views.settingweb, name='setting'),
    path('setting/update', views.updateSTW, name='update'),
    path('setting/choice/<str:type>/', views.choiceTrending, name='choice'),
]