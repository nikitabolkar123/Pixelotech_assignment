from django.urls import path

from . import views

urlpatterns = [
    path('registration/', views.UserRegistration.as_view(), name='user_registration'),
    path('users/<int:user_id>/',views. UserRegistration.as_view(), name='user-detail'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

]
