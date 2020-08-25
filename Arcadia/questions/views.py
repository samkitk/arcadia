import re
from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from account.models import Account
from .models import Question
from Arcadia.settings import START_TIME, END_TIME, MAX_QUESTIONS

def only_letters(answer):
    match = re.match("^[a-z]*$", answer)
    return bool(match)


class QuestionView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        current_time = datetime.now()

        if not START_TIME <= current_time <= END_TIME:
            messages.error(request, 'Arcadia is closed')
            return redirect('home')

        if request.user.get_current_que() == (MAX_QUESTIONS + 1):
            return redirect('congo')
        question_no = request.user.get_current_que()
        question = Question.objects.get(Question_Number=question_no)

        context = {'question': question}
        return render(request, 'questions.html', context)

    def post(self, request, *args, **kwargs):
        current_time = datetime.now()

        if not START_TIME <= current_time <= END_TIME:
            messages.error(request, 'Arcadia is closed')
            return redirect('home')

        question_no = request.user.get_current_que()
        question = Question.objects.get(Question_Number=question_no)

        answer = request.POST.get('answer')

        if not only_letters(answer):
            messages.error(
                request, 'Answer should only contain lower-case alphabets without spaces')
            return redirect('questions')
        if answer == question.Question_Answer:
            request.user.set_current_que()
            if request.user.get_current_que() == (MAX_QUESTIONS + 1):
                return redirect('congo')
            messages.info(request, 'Correct Answer!!')
            request.user.set_last_ans_time()
            return redirect('questions')
        else:
            messages.error(request, 'WrongAnswer!!')
            return redirect('questions')


@login_required
def congo_view(request, *args, **kwargs):

    if request.user.get_current_que() != (MAX_QUESTIONS + 1):
        messages.error(request, 'Complete all questions to get to that page!!')
        return redirect('home')
    return render(request, "congo.html", {})
