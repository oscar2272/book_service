from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('csrf/', views.get_csrf_token, name='csrf_token'),
    path('me/', views.current_user, name='user-list'),
]