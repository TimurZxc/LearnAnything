from django.urls import path,include
from .views import *

urlpatterns = [
    path('create-prompt/', GetPromptView.as_view()),
    path('signup/student/', StudentSignupView.as_view()),
    path('signup/mentor/', MentorSignupView.as_view()),
]