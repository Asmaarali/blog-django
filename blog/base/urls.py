from django.urls import path
from base import views

urlpatterns = [
    path('',views.index,name="index"),
    path('room/<str:pk>/',views.room,name="room"), #<str:pk> is the string and pk refers to key
    path('create-room',views.createroom,name="create-room"),
    path('update-room/<str:pk>/',views.updateroom,name="update-room"),
    path('delete-room/<str:pk>/',views.deleteroom,name="delete-room"),
    path('delete-message/<str:pk>/',views.deletemessage,name="delete-message"),
    path('profile/<str:pk>/',views.profile,name="user-profile"),
    path('update-profile/',views.updateprofile,name="update-profile"),
    path('all-topics/',views.alltopics,name="alltopics"),
    path('recent-activity/',views.recentactivity,name="recent-activity"),


    path('login/',views.loginpage,name="login"),
    path('logout/',views.logoutuser,name="logout"),
    path('register/',views.registerpage,name="register")
]

