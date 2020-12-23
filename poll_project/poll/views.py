from datetime import *


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .forms import CreatePollForm
from .models import Poll


def home(request):
    polls = Poll.objects.all()
    context = {
        "polls" : polls
    }
    return render(request,'poll/home.html', context)

def create(request):
    if request.method == "POST":
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:      
        form = CreatePollForm()
    context = {
        "form" : form
    }
    return render(request,'poll/create.html', context)

def vote(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except:
        messages.info(request, 'Requested poll does not exist!')
        return redirect("home")

    if request.method == "POST":
        selected_option = request.POST["poll"]
        if selected_option == "option1":
            poll.option_one_count += 1

            poll.date_lastvote = datetime.now()

        elif selected_option == "option2":
            poll.option_two_count += 1

            poll.date_lastvote = datetime.now()

        elif selected_option == "option3":
            poll.option_three_count += 1

            poll.date_lastvote = datetime.now()

        else:
            return HttpResponse(400, "Invalid form")

        poll.save()

        return redirect("results", poll.id)
    context = {
        "poll" : poll
    }
    return render(request,'poll/vote.html', context)

def results(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except:
        messages.info(request, 'Requested poll does not exist!')
        return redirect("home")

    context = {
        "poll" : poll
    }
    return render(request,'poll/results.html', context)