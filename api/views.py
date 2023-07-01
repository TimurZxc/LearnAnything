from .serializers import *
from .models import *
from rest_framework import generics, status
from rest_framework.response import Response
import openai
import json
from rest_framework.authtoken.models import Token

# Load your API key from an environment variable or secret management service
openai.api_key = "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"

class GetPromptView(generics.GenericAPIView):
    serializer_class = GetPromptSerializer

    def post(self, request, *args, **kwargs):
        prompt = "break down %s learning into step-by-step topics, starting with easy concepts and moving on to more complex ones. Generate a json list of topics in the following format: \"1\": \"Topic 1\",\"2\": \"topic 2\",\"3\": \"Topic 3\", and so on.  Where the number is the key and the topic name is the value. Make sure the list contains at least 25 topics. We will need to parse this json." % request.data.get('prompt')
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        response = json.loads(chat_completion["choices"][0]["message"]["content"])
        for topic in response:
            Topic.objects.create(name=response[topic])
        return Response(response,status=status.HTTP_200_OK)
    


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
