from .serializers import *
from .models import *
from rest_framework import generics, status, permissions
from rest_framework.response import Response
import openai
import json
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import *
from django.db.models import Q
from .youtube import *

# Load your API key from an environment variable or secret management service
openai.api_key = "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"


class TestKnowledgeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated & IsStudentUser]
    serializer_class = TestKnowledgeSerializer

    def post(self, request, *args, **kwargs):
        # try:
        course_name = request.data.get('prompt')
        student = Student.objects.get(user=request.user)
        course = Course.objects.create(
            name=course_name,
            student=student
        )
        prompt = "Create a test with 15 questions on the topic: %s. Each question have to be with 4 options and 1 correct answer. Test must be in the following format: [{\"title\": \"question itself\",\"variants\": [\"option 1\", \"option 2\", \"option 3\", \"option 4\"], \"correct\": index of the correct answer from variants list an int,},]. Make sure, that all keys and values enclosed in \" list must consist of 15 entities  and arrange every question in the same format" % course_name
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "system", "content": prompt}])
        response = json.loads(
            chat_completion["choices"][0]["message"]["content"])
        if Test.objects.filter(user=request.user).exists():
            Test.objects.all().delete()

        for question in response:
            Test.objects.create(
                user=request.user,
                course=course,
                title=question["title"],
                variants=question["variants"],
                correct=question["correct"]
            )

        return Response(response, status=status.HTTP_200_OK)


class GetTopicsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated & IsStudentUser]
    serializer_class = GetTopicsSerialiaer

    def post(self, request, *args, **kwargs):
        course_name = request.data.get('prompt')
        answers = request.data.get('answers')
        course = Course.objects.filter(name=course_name).first()
        test = Test.objects.filter(user=request.user)
        form_data = {}
        for index, i in enumerate(test, start=0):
            helper = {
                "a": i.variants[1:-1].split("'")[1],
                "b": i.variants[1:-1].split("'")[3],
                "c": i.variants[1:-1].split("'")[5],
                "d": i.variants[1:-1].split("'")[7]
            }
            form_data.update({f"question {i.id}": i.title})
            form_data.update({f"answer {i.id}": helper[answers[index]]})
        prompt_for_topics = f"break down {course} learning into step-by-step topics based on the results of this test: {form_data}, starting with easy concepts and moving on to more complex ones. Generate a json list of topics in the following format: \"1\": \"Topic 1\",\"2\": \"topic 2\",\"3\": \"Topic 3\", and so on.  Where the number is the key and the topic name is the value. Make sure the list contains at least 25 topics. We will need to parse this json. Your response must be only JSON, without any greetings etc."
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "system", "content": prompt_for_topics}])
        response = json.loads(chat_completion["choices"][0]["message"]["content"])
        for topic in response:
            Topic.objects.create(name=response[topic], course=course)
        first = Topic.objects.filter(course=course).first()
        first.is_opened = True
        first.save()

        prompt_for_topic_data = 'Provide me three actual article sources for learning "' + course_name + ':'+ first.name + '". It has to be in JSON format: {\{"1": "source_url1", "2": "source_url2", "3": "source_url3"}\}. Your response must be only JSON, without any greetings, etc.'
        
        video_ids = get_videos(search_query=f"{course_name}: {first.name} tutorials")

        generation_topic_data = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "system", "content": prompt_for_topic_data}])
        topic_data_response = json.loads(generation_topic_data["choices"][0]["message"]["content"])
        for i, video in enumerate(video_ids, start=1):
            link = "https://www.youtube.com/embed/" + video
            Video.objects.create(link=link, topic=first)
            Source.objects.create(link=topic_data_response[str(i)], topic=first)

        prompt_for_topic_quiz = 'Create test with range of questions 10 - 20, with this topic: "' + course_name + ':'+ first.name + '". Each question have to be with 4 options and 1 correct answer. This test must be in JSON format:  [{\"title\": \"question itself\",\"variants\": [\"option 1\", \"option 2\", \"option 3\", \"option 4\"], \"correct\": index of the correct answer from variants list an int,},] list must consist of 15 entities  and arrange every question in the same format"'
        generation_quiz_data = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "system", "content": prompt_for_topic_quiz}])
        topic_quiz_responcse = json.loads(generation_quiz_data["choices"][0]["message"]["content"])
        quiz = Quiz.objects.create(topic=first)
        for question in topic_quiz_responcse:
            Question.objects.create(
                quiz=quiz,
                title=question["title"],
                variants=question["variants"],
                correct=question["correct"]
            )
        return Response(topic_quiz_responcse, status=status.HTTP_200_OK)


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


class GetDataView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, *args, **kwargs):
        user = User.objects.filter(id=self.request.user.id)
        # courses = Course.objects.filter(student=student)
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.data.get('email'))
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data)

class FinishQuizView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated & IsStudentUser]
    serializer_class = FinishQuizSerializer

    def post(self, request, *args, **kwargs):
        answers = request.data.get('answers')
        topic = Topic.objects.filter(is_opened = True).last()
        quiz = Quiz.objects.get(topic=topic)
        questions = Question.objects.filter(quiz=quiz)
        topic_next = Topic.objects.get(id=topic.id + 1)
        correct = 0
        helper = {
            "a":0,
            "b":1,
            "c":2,
            "d":3
        }
        for question in questions:
            if helper[answers[question.id - 1]] == question.correct:
                correct += 1
        if (correct*100)/len(questions) >= 70:
            topic_next.is_opened = True
            topic_next.save()
            course = Course.objects.get(id=topic.course.id)

            prompt_for_topic_data = 'Provide me three actual article sources for learning "' + course.name + ':'+ topic_next.name + '". It has to be in JSON format: {\{"1": "source_url1", "2": "source_url2", "3": "source_url3"}\}. Your response must be only JSON, without any greetings, etc.'
            video_ids = get_videos(search_query=f"{course.name}: {topic_next.name} tutorials")
            generation_topic_data = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "system", "content": prompt_for_topic_data}])
            topic_data_response = json.loads(generation_topic_data["choices"][0]["message"]["content"])

            for i, video in enumerate(video_ids, start=1):
                link = "https://www.youtube.com/embed/" + video
                Video.objects.create(link=link, topic=topic_next)
                Source.objects.create(link=topic_data_response[str(i)], topic=topic_next)

            prompt_for_topic_quiz = 'Create test with range of questions 10 - 20, with this topic: "' + course.name + ':'+ topic_next.name + '". Each question have to be with 4 options and 1 correct answer. This test must be in JSON format:  [{\"title\": \"question itself\",\"variants\": [\"option 1\", \"option 2\", \"option 3\", \"option 4\"], \"correct\": index of the correct answer from variants list an int,},] list must consist of 15 entities  and arrange every question in the same format"'
            generation_quiz_data = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "system", "content": prompt_for_topic_quiz}])
            topic_quiz_responcse = json.loads(generation_quiz_data["choices"][0]["message"]["content"])
            quiz = Quiz.objects.create(topic=topic_next)
            for question in topic_quiz_responcse:
                Question.objects.create(
                    quiz=quiz,
                    title=question["title"],
                    variants=question["variants"],
                    correct=question["correct"]
                )

            return Response({"message": "Topic Completed Successfully",},status=status.HTTP_200_OK)
        else:
            return Response({"message": "Topic Failed",},status=status.HTTP_200_OK)

        