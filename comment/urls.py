from django.urls import path
from comment import views

app_name = 'comment'
urlpatterns = [
    path('<int:video_type>/comment_home', views.comment_home, name = 'comment_home'),
    path('<int:video_id>/comment_main/', views.comment_main, name = 'comment_main'),
    path('<int:cmt_id>/delete/', views.delete_comment, name = 'delete_comment'),
    # path('<int:report_id>/update/', views.detail_report, name = 'detail_report'),
]