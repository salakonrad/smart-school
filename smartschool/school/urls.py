from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name="index"),
    # Classes
    path('classes', views.class_list_view, name="class_list"),
    path('classes/add', views.class_add, name="class_add"),
    path('classes/delete', views.class_delete, name="class_delete"),
    path('classes/change', views.class_change, name="class_change"),
    # Class Profiles
    path('class_profile', views.class_profile_list_view, name="class_profile_list"),
    path('class_profile/add', views.class_profile_add, name="class_profile_add"),
    path('class_profile/delete', views.class_profile_delete, name="class_profile_delete"),
    path('class_profile/change', views.class_profile_change, name="class_profile_change"),
    # Students
    path('students', views.student_list_view, name="student_list"),
    path('students/details/<str:id>', views.student_view, name="student"),
    path('students/add', views.student_add, name="student_add"),
    # Authorization
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/logout/', views.logout_view, name="logout")
]