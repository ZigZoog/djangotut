from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Choice, Question
# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    front_end_stuff = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', front_end_stuff)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html',{'question':question})


def results(requestion, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        #redisplay voting form.
        return render(request, 'polls/detail.html',{'question':question,'error_message':"You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #always return HTTP response after successly dealing
        #with POST data. this prevents data from being posted twice if a user hits the Back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
