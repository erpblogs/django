from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F

from .models import Question, Choice


# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # output = ', '.join([q.question_text for q in latest_question_list])

    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     return render(request, 'polls/page_404.html', {})
    #     raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
    # return HttpResponse(f"You are looking at question {question_id}!")


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
    # return HttpResponse(f"You are looking at the result of question {question_id}!")


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
