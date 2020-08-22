from django.urls import path
from .views import (HomePageView, LoginView, RegisterView, 
					ActivateView, instruction_view, leaderboard_view,
					logout_view)

urlpatterns = [
	path('', HomePageView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', ActivateView.as_view(), name='activate'),
    path('instruction/', instruction_view, name='instructions'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
	path('logout/', logout_view, name='logout'),
]