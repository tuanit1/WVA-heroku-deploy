from django.urls import path
from report import views

app_name = 'report'
urlpatterns = [
    path('<int:video_type>/report_home', views.report_home, name = 'report_home'),
    path('<int:video_id>/report_main/', views.report_main, name = 'report_main'),
    path('<int:report_id>/update/', views.detail_report, name = 'detail_report'),
    path('<int:report_id>/delete/', views.delete_report, name = 'delete_report'),
]