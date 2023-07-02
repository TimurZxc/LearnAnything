from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TestKnowledgeSerializer(serializers.ModelSerializer):
    prompt = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    class Meta:
        fields = ['prompt']

class GetTopicsSerialiaer(serializers.ModelSerializer):
    answers = serializers.CharField(max_length = 15, style={'input_type': 'text'}, write_only=True)
    prompt = serializers.CharField(style={'input_type': 'text'}, write_only=True)

    class Meta:
        fields = ['answers', 'prompt']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','title', 'variants', 'correct']

class QuizSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True)
    class Meta:
        model = Quiz
        fields = ['id','question']

class SourceLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id','link']

class VideoLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id','link']

class TopicSerializer(serializers.ModelSerializer):
    video = VideoLinkSerializer(many=True)
    source = SourceLinkSerializer(many=True)
    quiz = QuizSerializer(many=True)
    class Meta:
        model = Topic
        fields = ['id','name', 'is_opened', 'is_finished','video','source','quiz']

class CoursesSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id','name', 'student', 'topic']
        
class StudentSerializer(serializers.ModelSerializer):
    course = CoursesSerializer(many=True)
    class Meta:
        model = Student
        fields = ['id','birth_date', 'course']

class UserSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False)
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'surname', 'email', 'is_student', 'is_mentor', 'student']

class StudentSignupSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password2', 'surname', 'birth_date']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self, *args, **kwargs):
        user = User.objects.create_user(
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            email = self.validated_data['email'],
            surname = self.validated_data['surname'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'error': 'Passwords must match.'})
        user.set_password(password)
        user.is_student = True
        user.is_active = True
        user.save()
        student = Student.objects.create(
            birth_date = self.validated_data['birth_date'],
            user = user
        )
        student.save()
        return user
    
class MentorSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password2', 'surname']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self, *args, **kwargs):
        user = User.objects.create_user(
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            email = self.validated_data['email'],
            surname = self.validated_data['surname'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'error': 'Passwords must match.'})
        user.set_password(password)
        user.is_mentor = True
        user.is_active = True
        user.save()
        mentor = Mentor.objects.create(
            user=user
        )
        mentor.save()
        return user
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    remember = serializers.BooleanField(default=False)
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['is_mentor'] = user.is_mentor
        token['is_student'] = user.is_student
        return token
    
class FinishTopicSerializer(serializers.ModelSerializer):
    name = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    class Meta:
        model = Topic
        fields = ['name']

class FinishQuizSerializer(serializers.ModelSerializer):
    answers = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    class Meta:
        model = Quiz
        fields = ['answers']

