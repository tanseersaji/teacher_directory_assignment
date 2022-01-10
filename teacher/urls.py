from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_teachers, name='view_all_teachers'),
    path('<int:teacher_id>/', views.teacher_details, name='view_teacher_details'),
    path('bulk_add/', views.bulk_add_teachers, name='view_bulk_add_teachers'),

    path('accounts/register/', views.register, name='register'),
]
