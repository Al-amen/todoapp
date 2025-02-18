from django.urls import path
from django.contrib.auth import  views as auth_view
from todoapp import views
urlpatterns = [

    path('login/', auth_view.LoginView.as_view(template_name = "todoapp/login.html"), name='login'),
    path('authenticate/<str:token>/',views.authenticate_via_magic_link,name='authenticate'),
    path('register/',views.register,name='register'),
    path('hello/', views.hello_protected, name='hello_protected'),
    path('logout/', views.user_logout, name='logout'),
    path('task/', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    
   

  
    
    
]
