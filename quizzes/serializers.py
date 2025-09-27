from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Quiz, Question, QuizResult

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'topic', 'num_questions', 'difficulty', 'created_at', 'questions', 'user']

class QuizResultSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = QuizResult
        fields = ['id', 'quiz', 'score', 'completed_at', 'answers', 'user']