from django.urls import path
from .views import QuestionView, congo_view


urlpatterns = [
	path('questions/', QuestionView.as_view(), name='questions'),
    path('congratulations/', congo_view, name='congo'),
]