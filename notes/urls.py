from django.urls import path
from . import views


urlpatterns = [
    path('',views.index),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('user/',views.user,name='user'),
    path('upload/',views.upload,name='upload'),
    path('edit/<int:pk>/',views.pdfedit,name='edit'), 
    path('delete/<int:pk>/',views.delete,name='delete'), 
    path('uploaddash/',views.uploaddash,name='uploaddash'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('logouts/',views.logouts,name='logouts'),
    path('profile/',views.editprofile,name='profile'),
    path('profilee/',views.profilee,name='profilee'),
    path('not/',views.notifications,name='not'),
    path('search/',views.search, name='search'),  
    path('post/<int:post_id>/add-to-favorites/',views.add_to_favorites, name='add_to_favorites'),
    path('favorites/',views.favorites, name='favorites'),
    #courses
    path('uploadcourse/',views.upload_course,name='courseupload'),
    path('deletecourse/',views.delete_course,name='deletecourse'),
    path('editcourse/<slug:slug>/',views.edit_course, name='edit_course'),
    path('courselist/',views.course_list,name='course_list'),
    path('course_detail/<slug:slug>/',views.course_detail, name='course_detail'),
    path('coursedash/',views.coursedash,name='coursedash'),
    #videos
    path('course/<int:course_id>/video/upload/', views.upload_video, name='upload_video'),
    path('course/<int:course_id>/video/<int:video_id>/edit/', views.edit_video, name='edit_video'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    
    # Learning URLs
    path('learning/', views.learning_list, name='learning_list'),
    path('learning/create/', views.learning_create, name='learning_create'),
    path('learning/<int:learning_id>/', views.learning_detail, name='learning_detail'),
    path('learning/<int:learning_id>/update/', views.learning_update, name='learning_update'),
    path('learning/<int:learning_id>/delete/', views.learning_delete, name='learning_delete'),

    # Tag URLs
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/create/', views.tag_create, name='tag_create'),
    path('tags/<int:tag_id>/', views.tag_detail, name='tag_detail'),
    path('tags/<int:tag_id>/update/', views.tag_update, name='tag_update'),
    path('tags/<int:tag_id>/delete/', views.tag_delete, name='tag_delete'),

    # Prerequisite URLs
    path('prerequisites/', views.prerequisite_list, name='prerequisite_list'),
    path('prerequisites/create/', views.prerequisite_create, name='prerequisite_create'),
    path('prerequisites/<int:prerequisite_id>/', views.prerequisite_detail, name='prerequisite_detail'),
    path('prerequisites/<int:prerequisite_id>/update/', views.prerequisite_update, name='prerequisite_update'),
    path('prerequisites/<int:prerequisite_id>/delete/', views.prerequisite_delete, name='prerequisite_delete'),

    #admin dash
    path('admin1/',views.admin1,name='admin1'),
    
    #chatbot
    path('chat/', views.chatbot, name='chatbot'),

]