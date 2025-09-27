from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Quiz, Question, QuizResult
from .serializers import QuizSerializer, QuizResultSerializer, QuestionSerializer
import google.generativeai as genai
import os
import json

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel(model_name='gemini-2.0-flash')

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    if not (username and email and password):
        return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username, email, password)
    return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_quiz(request):
    topic = request.data.get('topic')
    num_questions = int(request.data.get('num_questions', 5))
    difficulty = request.data.get('difficulty', 'easy')
    
    if num_questions < 5 or num_questions > 20:
        return Response({'error': 'Questions must be 5-20'}, status=status.HTTP_400_BAD_REQUEST)
    
    prompt = f"Generate {num_questions} multiple-choice questions on '{topic}' at {difficulty} level. Each question should have 4 options (A,B,C,D) and indicate the correct one. Format strictly as JSON array: [{{\"question\": \"text\", \"a\": \"optA\", \"b\": \"optB\", \"c\": \"optC\", \"d\": \"optD\", \"correct\": \"A\"}}, ...]. No extra text."
    
    try:
        response = model.generate_content(prompt)
        questions_text = response.text.strip().strip('```json').strip('```')
        questions_data = json.loads(questions_text)
    except Exception as e:
        return Response({'error': f'AI generation failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    quiz = Quiz.objects.create(
        user=request.user,
        topic=topic,
        num_questions=num_questions,
        difficulty=difficulty
    )
    
    for q_data in questions_data:
        Question.objects.create(
            quiz=quiz,
            text=q_data.get('question'),
            option_a=q_data.get('a'),
            option_b=q_data.get('b'),
            option_c=q_data.get('c'),
            option_d=q_data.get('d'),
            correct_option=q_data.get('correct')
        )
    
    serializer = QuizSerializer(quiz)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class QuizListView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quiz(request, pk):
    try:
        quiz = Quiz.objects.get(pk=pk, user=request.user)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz(request, pk):
    try:
        quiz = Quiz.objects.get(pk=pk, user=request.user)
        user_answers = request.data.get('answers', {})
        score = 0
        
        for q_id, user_choice in user_answers.items():
            question = Question.objects.get(id=q_id, quiz=quiz)
            if user_choice.upper() == question.correct_option:
                score += 1
        
        result = QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            answers=user_answers
        )
        
        serializer = QuizResultSerializer(result)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ResultListView(generics.ListAPIView):
    serializer_class = QuizResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QuizResult.objects.filter(user=self.request.user)