from django.urls import path
from . import views
app_name = 'category'
urlpatterns = [
    path('category/<str:pk>/', views.category, name='category'),
    path('category-add/<str:pk>/', views.addCategory, name='add'),
    path('category-edit/<str:pk>/<str:id>', views.editCategory, name='edit'),
    path('category/<str:pk>/<str:id>', views.disableCategory, name='delcate'),
]