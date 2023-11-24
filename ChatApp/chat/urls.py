from django.urls import path, include
from chat import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView
 
 
urlpatterns = [
    path("", chat_views.chatPage, name="chat-page"),
    path('<str:room_name>/', chat_views.room, name='chat-room'),
    path('getMessages/<str:room_name>/', chat_views.getMessages, name='getMessages'),
    path("checkview", chat_views.checkview, name="checkview"),
    path("send", chat_views.send, name="send"),
    path('register', chat_views.register, name='register'),
    path('login', chat_views.login, name='login'),
    path('logout', chat_views.logout, name='logout'),
]