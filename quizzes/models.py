from django.db import models
from django.contrib.auth.models import User  # Built-in User

class Quiz(models.Model):
    DIFFICULTY_CHOICES = [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    num_questions = models.IntegerField(default=5)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} Quiz - {self.difficulty}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1)  # 'A', 'B', etc.

    def __str__(self):
        return str(self.text)[:50]

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()  # e.g., 8/10
    completed_at = models.DateTimeField(auto_now_add=True)
    answers = models.JSONField(default=dict)  # Store user choices for review

    def __str__(self):
        return f"{self.user.username} - {self.score}/10 on {self.quiz.topic}"