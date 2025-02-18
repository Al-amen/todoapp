from django.urls import path

from media_app import views
app_name = "media_app"
urlpatterns = [
    path('', views.media_list, name='media_list'),  # list all media files uploaded by the user
    path('upload/',views.media_upload,name='media_upload'),
    path('edit/<int:pk>/', views.media_edit, name='media_edit'),  # edit a specific media file by its primary key
    path('delete/<int:pk>/', views.media_delete, name='media_delete'),  # delete a specific media file by its primary key
    
]

  
