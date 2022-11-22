from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import F

from .models import Question, Choice
import json
import requests
import pickle
import os

current_path = os.path.dirname(__file__)

from pathlib import Path

website_domain = '*****************'
COOKIE_FILE = 'cookie.txt'
filename = os.path.join(current_path, COOKIE_FILE)


# COOKIE_FILE = 'cookie.txt'


def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)


def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     # output = ', '.join([q.question_text for q in latest_question_list])
#
#     # return HttpResponse(template.render(context, request))
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     return render(request, 'polls/page_404.html', {})
#     #     raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})
#     # return HttpResponse(f"You are looking at question {question_id}!")
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
#     # return HttpResponse(f"You are looking at the result of question {question_id}!")


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # FIRST SOLUTION
        # selected_choice.votes += 1
        # SECOND SOLUTION

        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # F() assignments persist after Model.save()
        # This persistence can be avoided by reloading the model object after saving it,
        # for example, by using refresh_from_db().
        selected_choice.refresh_from_db()
        # selected_choice.save()

        # THIRD SOLUTION
        # selected_choice.update(stories_filed=F('votes') + 1)

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def applicant(request):
    session = requests.Session()
    # response = session.get('http://google.com')

    headers = {
        "Content-Type": "application/json",
    }

    # payload = {
    #     "jsonrpc": "2.0",
    #     "method": "call",
    #     "id": 0,
    #     "params": {
    #         "db": "***********",
    #         "login": "***********",
    #         "password": "***********"
    #     },
    # }
    # response = session.get(f"{website_domain}/web/session/authenticate", data=json.dumps(payload),
    #                        headers={"Content-Type": "application/json"})
    #
    # save_cookies(session.cookies, COOKIE_FILE)

    # print(session.cookies.get_dict())

    applicant_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params":
            {
                "model": "ir.attachment",
                "fields": [],
                "domain": [["mimetype", "=", "application/pdf"]],
                "limit": 10
            }
    }

    # headers.update({"cookie": json.dumps({'session_id': 'ecc8ef53ec90f619b865edd7eff30219b268b352'})})

    applicant = requests.get(f"{website_domain}/web/dataset/search_read", data=json.dumps(applicant_payload),
                             headers=headers, cookies=load_cookies(filename))

    return render(request, 'polls/applicant.html', {'applicants': applicant.json().get('result').get('records')})
    # return HttpResponseRedirect(reverse('polls:applicant', args=(applicant)))
