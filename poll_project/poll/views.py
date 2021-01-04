#from datetime import *
import rest_framework
import json


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import CreatePollForm
from .models import Poll


@csrf_exempt
def home(request):
    polls = Poll.objects.all()
    response = serializers.serialize('json', polls)
    return HttpResponse(response, content_type="text/json")

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
                    empty"""}]), content_type="text/json")

        except:
            return HttpResponse(json.dumps([{"Error": "Fields: \'question\', \'option_one\', \'option_two\', \'option_three\' must be defined"}]), 
                content_type="text/json")



            #poll.date_lastvote = datetime.now()

@csrf_exempt
def vote(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except:
        return HttpResponse(json.dumps([{"Error": "Poll requested doesn't exist!"}]), content_type="text/json")

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
            return HttpResponse(json.dumps([{"Error": "Option out of valid range!"}]), content_type="text/json")
        else:
            return HttpResponse(json.dumps([{"Success": "Vote posted!"}]), content_type="text/json")
        
@csrf_exempt
def results(request, poll_id):
    response = None
    try:
        poll = Poll.objects.get(pk=poll_id)
        response = json.dumps([{ "question": poll.question, "option_one": poll.option_one, "option_two": poll.option_two, "option_three": poll.option_three,
            "option_one_count": poll.option_one_count, "option_two_count": poll.option_two_count, "option_three_count": poll.option_three_count}])     
        
        return HttpResponse(response, content_type="text/json")
    except:
        return HttpResponse(json.dumps([{"Error": "Poll requested doesn't exist!"}]), content_type="text/json")
