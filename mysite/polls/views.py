from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Choice, Question,Vote
from django.views import generic
from django.utils import timezone
from account.models import Account
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth import logout as logouts
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_user_list'

    def get_queryset(self):
        """Return the users."""
        return Account.objects.annotate(Count('question')).order_by('-question__count')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required()
def user(request, user_id):
    latest_question_list = Question.objects.filter(user = user_id).order_by('-popularity')
    u = Account.objects.get(pk = user_id)
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/user.html', context)

@login_required()
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        if not question.user_can_vote(request.user):
            return render(request, 'polls/results.html', {
            'question': question,
            'error_message': "You've already voted.",
        })
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.question.popularity+=1
        selected_choice.save()
        selected_choice.question.save()
        vote = Vote(user=request.user, question = question, choice = selected_choice)
        vote.save()
        print(vote)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('polls:login')