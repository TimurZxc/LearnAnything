from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-topics/', GetTopicsView.as_view()),
    path('signup/student/', StudentSignupView.as_view()),
    path('signup/mentor/', MentorSignupView.as_view()),
    path('login/', MyTokenObtainPairView.as_view()),
    path('test/', TestKnowledgeView.as_view()),
    path('data/', GetDataView.as_view()),
    path('finish/quiz/', FinishQuizView.as_view()),
]