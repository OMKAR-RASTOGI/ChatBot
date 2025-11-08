# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('get-response/', views.get_response, name='get_response'),
#     path('signup/', views.signup_view, name='signup'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('clear/', views.clear_chat, name='clear_chat'),
]
