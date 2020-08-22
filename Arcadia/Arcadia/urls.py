"""BrandHunt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account.views import HomePageView, LoginView, logout_view, instruction_view, leaderboard_view, ActivateView, RegisterView
from questions.views import QuestionView, congo_view
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', ActivateView.as_view(), name='activate'),
    path('instruction/', instruction_view, name='instructions'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('admin/', admin.site.urls),
    path('logout/', logout_view, name='logout'),
    path('questions/', QuestionView.as_view(), name='questions'),
    path('congratulations/', congo_view, name='congo'),
    #path('static/', )
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
