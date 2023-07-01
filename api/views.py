from .serializers import *
from .models import *
from rest_framework import generics, status, permissions
from rest_framework.response import Response
import openai
import json
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import *

# Load your API key from an environment variable or secret management service
openai.api_key = "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"


class TestKnowledgeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated & IsStudentUser]
    serializer_class = TestKnowledgeSerializer

    def post(self, request, *args, **kwargs):
        try:
            course_name = request.data.get('prompt')
            prompt = "Create a test with 15 questions on the topic: %s. Each question have to be with 4 options and 1 correct answer. Test must be in the following JSON format: {\"question 1\": { \"question\" : \"The question itself\",\"option 1\" : \"option 1 itself\",\"option 2\" : \"option 2 itself\",\"option 3\" : \"option 3 itself\",\"option 4\" : \"option 4 itself\",\"correct\" : \"correct option key\"}} and arrange every question in the same format" % course_name
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
            response = json.loads(chat_completion["choices"][0]["message"]["content"])
            print(response)
            for question in response:
                Test.objects.create(
                    user=request.user, 
                    course=course_name,
                    question=response[question]["question"],
                    option_1 = response[question]["option 1"], 
                    option_2 = response[question]["option 2"], 
                    option_3 = response[question]["option 3"], 
                    option_4 = response[question]["option 4"], 
                    correct = response[question]["correct"]
                )
            student = Student.objects.get(user=request.user)
            Course.objects.create(
                name=course_name,
                student=student
            )
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTopicsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated & IsStudentUser]
    serializer_class = GetTopicsSerialiaer

    def post(self, request, *args, **kwargs):
        course_name = request.data.get('prompt')
        print(course_name)
        course = Course.objects.filter(name=course_name).first()
        print(course)
        test = Test.objects.filter(course_id=course)
        print(test)
        # prompt = f"break down {course} learning into step-by-step topics based on the results of the test, starting with easy concepts and moving on to more complex ones. Generate a json list of topics in the following format: \"1\": \"Topic 1\",\"2\": \"topic 2\",\"3\": \"Topic 3\", and so on.  Where the number is the key and the topic name is the value. Make sure the list contains at least 25 topics. We will need to parse this json."
        # chat_completion = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        # response = json.loads(chat_completion["choices"][0]["message"]["content"])
        # for topic in response:
        #     Topic.objects.create(name=response[topic], course = course)
        return Response(status=status.HTTP_200_OK)

class StudentSignupView(generics.CreateAPIView):
    serializer_class = StudentSignupSerializer

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "Student Created Successfully"
        })


class MentorSignupView(generics.CreateAPIView):
    serializer_class = MentorSignupSerializer

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "Mentor Created Successfully"
        })

# Login/Logout Views


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
