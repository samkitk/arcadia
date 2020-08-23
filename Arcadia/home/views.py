from django.shortcuts import render

from account.models import Account
# Create your views here.


def home_page_view(request, *args, **kwargs):
    context = {}
    return render(request, "home/home.html", context)

def leaderboard_view(request, *args, **kwargs):
    users = Account.objects.filter(is_superuser=False).order_by('-current_que','last_ans_time')
    context = {'users': users}
    return render(request, 'leaderboard.html', context)


def instruction_view(request, *args, **kwargs):
    context = {}
    return render(request, 'instructions.html', context)