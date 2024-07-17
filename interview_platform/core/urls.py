from django.urls import path
from .views import login_view, register_view, interview_get_view, interview_api_view, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('interview/', interview_get_view, name='interview'),
    path('api/interview/', interview_api_view, name='interview_api'),
]