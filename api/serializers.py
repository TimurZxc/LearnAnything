from rest_framework import serializers
from .models import *

class GetPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ['prompt']

    def save(request):
        prompt = Prompt.objects.create(
            prompt = request.data.prompt
        )
        prompt.save()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'surname', 'email', 'is_student', 'is_mentor']

class StudentSignupSerializer(serializers.ModelSerializer):

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
        user.is_student = True
        user.is_active = True
        user.save()
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
        return user