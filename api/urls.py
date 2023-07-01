from django.urls import path,include
from .views import *

urlpatterns = [
    path('get-topics/', GetTopicsView.as_view()),
    path('signup/student/', StudentSignupView.as_view()),
    path('signup/mentor/', MentorSignupView.as_view()),
    path('login/', MyTokenObtainPairView.as_view()),
    path('test/', TestKnowledgeView.as_view()),
]