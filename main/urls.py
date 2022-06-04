from django.urls import path
from main import views
app_name = 'main'
urlpatterns = [
    path('', views.login_view),
    path('logout/', views.logoutPage, name='logout'),
]