from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect
from django.template import loader
# from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

"""
#기존 뷰 작성
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id) #get()을 사용해 Http404예외 발생시키기, 단축 기능 사용
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
"""
class IndexView(generic.ListView):
    template_name = 'polls/index.html' #기존의 템플릿을 사용하기 위해 ListView에 template_name 전달
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

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) #선택된 설문의 ID를 문자열로 반환
    except (KeyError, Choice.DoesNotExist): #POST 자료에 choice가 없을 때 keyError 발생
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', { #에러 메시지 + 설문조사 폼 다시 보여줌
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,))) #ex: /polls/3/results/ 문자열 반환
