from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('quizzes/', views.QuizListView.as_view(), name='quiz-list'),
    path('quizzes/create/', views.create_quiz, name='create-quiz'),
    path('quizzes/<int:pk>/', views.get_quiz, name='get-quiz'),
    path('quizzes/<int:pk>/submit/', views.submit_quiz, name='submit-quiz'),
    path('results/', views.ResultListView.as_view(), name='result-list'),
]