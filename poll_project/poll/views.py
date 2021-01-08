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
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.parsers import JSONParser 
from rest_framework import serializers 



from .forms import CreatePollForm
from .models import Poll
from .serializers import *



@csrf_exempt
def home(request):
    polls = Poll.objects.all()
    response = serializers.serialize('json', polls)
    return HttpResponse(response, content_type="text/json")


class PollList(ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class ResultsPollList(RetrieveAPIView):
    #queryset = Poll.objects.get(pk=1)
    #queryset = Poll.objects.all()
    lookup_url_kwarg = "poll_id"
    serializer_class = ResultsPollSerializer

    def get_queryset(self):
        poll_id = self.kwargs["poll_id"]
        poll = Poll.objects.filter(pk=poll_id)
        return poll

# class VotePollList(RetrieveAPIView):
#     #queryset = Poll.objects.get(pk=1)
#     #queryset = Poll.objects.all()
#     lookup_url_kwarg = "poll_id"
#     serializer_class = VotePollSerializer

#     def get_queryset(self):
#         poll_id = self.kwargs["poll_id"]
#         poll = Poll.objects.filter(pk=poll_id)
#         return poll


class VotePollList(generics.RetrieveUpdateAPIView):
    lookup_url_kwarg = "poll_id"
    serializer_class = VotePollSerializer

    def get_queryset(self):
        poll_id = self.kwargs["poll_id"]
        poll = Poll.objects.filter(pk=poll_id)

        return poll
    def put(self, request, poll_id):
        print(request.data)

        poll = Poll.objects.get(pk=poll_id)

        option_one_count = poll.option_one_count
        option_two_count = poll.option_two_count
        option_three_count = poll.option_three_count
        
        request_data = request.data.copy()



        only_one_true = (request_data["option_one_count"]=="1") + (request_data["option_two_count"]=="1")+(request_data["option_three_count"]=="1")
        print(only_one_true)
        if (only_one_true == 1):
            request_data["option_one_count"] = str(int(request_data["option_one_count"]) + option_one_count)
            request_data["option_two_count"] = str(int(request_data["option_two_count"]) + option_two_count)
            request_data["option_three_count"] = str(int(request_data["option_three_count"]) + option_three_count)
        else:
            raise serializers.ValidationError({"detail": "Option must be an increment of 1"})

        poll_serializer = VotePollSerializer(poll, data=request_data)
        if poll_serializer.is_valid():            
            poll_serializer.save()
            return JsonResponse(poll_serializer.data) 

            
        return JsonResponse(poll_serializer.errors, status=400) 






@csrf_exempt
def create(request):
    if request.method == "POST":
        data = json.loads(request.body)  
        try:
            question = data["question"]
            option_one = data["option_one"]
            option_two = data["option_two"]
            option_three = data["option_three"]
            

            try:
                poll = Poll.objects.create()
                poll.question = question
                poll.option_one = option_one
                poll.option_two = option_two
                poll.option_three = option_three
                poll.save()

                return HttpResponse(json.dumps([{"Success": "Poll created!"}]), content_type="text/json")
            except:
                return HttpResponse(json.dumps([{"""Error": "Fields: \'question\', \'option_one\', \'option_two\', \'option_three\' can not be left 
                    empty"""}]), content_type="text/json", status=400)

        except:
            return HttpResponse(json.dumps([{"Error": "Fields: \'question\', \'option_one\', \'option_two\', \'option_three\' must be defined"}]), 
                content_type="text/json", status=400)
    else:
        return HttpResponse(json.dumps([{}]), content_type="text/json")


            #poll.date_lastvote = datetime.now()

@csrf_exempt
def vote(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except:
        return HttpResponse(json.dumps([{"Error": "Poll requested doesn't exist!"}]), content_type="text/json", status=400)

    if request.method == "GET":
        response = json.dumps([{ "question": poll.question, "option_one": poll.option_one, "option_two": poll.option_two, "option_three": poll.option_three}])     
        return HttpResponse(response, content_type="text/json")
    elif request.method == "POST":
        error = None
        data = json.loads(request.body)
        selected_option = data["option"]

        if selected_option == 1:
            poll.option_one_count += 1
            poll.save()
            #poll.date_lastvote = datetime.now()

        elif selected_option == 2:
            poll.option_two_count += 1
            poll.save()
            #poll.date_lastvote = datetime.now()

        elif selected_option == 3:
            poll.option_three_count += 1
            poll.save()
            #poll.date_lastvote = datetime.now()

        else:
            error = 1

        if error ==  1:
            return HttpResponse(json.dumps([{"Error": "Option out of valid range!"}]), content_type="text/json", status=400)
        else:
            return HttpResponse(json.dumps([{"Success": "Vote posted!"}]), content_type="text/json")
        
@csrf_exempt
def results(request, poll_id):
    response = None
    try:
        poll = Poll.objects.get(pk=poll_id)
        # response = json.dumps([{ "question": poll.question, "option_one": poll.option_one, "option_two": poll.option_two, "option_three": poll.option_three,
        #     "option_one_count": poll.option_one_count, "option_two_count": poll.option_two_count, "option_three_count": poll.option_three_count}])     
        
        # return HttpResponse(response, content_type="text/json")

        response = serializers.serialize('json', [poll])
        return HttpResponse(response, content_type="text/json")

    except Poll.DoesNotExist:
        return HttpResponse(json.dumps([{"Error": "Poll requested doesn't exist!"}]), content_type="text/json", status=400)



