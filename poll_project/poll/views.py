from datetime import *
import rest_framework
import json


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core import serializers
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, serializers 
from rest_framework.parsers import JSONParser 
from rest_framework import serializers 



from .forms import CreatePollForm
from .models import Poll
from .serializers import *



class PollList(ListAPIView):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()


class PollResults(RetrieveAPIView):
    lookup_url_kwarg = "poll_id"
    serializer_class = ResultsPollSerializer    
    queryset = Poll.objects.all()

class PollVote(generics.RetrieveUpdateAPIView):
    lookup_url_kwarg = "poll_id"
    serializer_class = ResultsPollSerializer
    queryset = Poll.objects.all()

class CreatePoll(CreateAPIView):
    serializer_class = PollSerializer







