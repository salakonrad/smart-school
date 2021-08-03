from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name="index"),
    path('classes', views.class_list_view, name="class_list"),
    # Authorization
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/logout/', views.logout_view, name="logout")
]