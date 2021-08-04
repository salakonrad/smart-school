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
    path('class_profiles', views.class_profiles_list_view, name="class_profiles_list"),
    # path('class_profiles/add', views.class_profiles_add, name="class_profiles_add"),
    # path('class_profiles/delete', views.class_profiles_delete, name="class_profiles_delete"),
    # path('class_profiles/change', views.class_profiles_change, name="class_profiles_change"),
    # Authorization
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/logout/', views.logout_view, name="logout")
]