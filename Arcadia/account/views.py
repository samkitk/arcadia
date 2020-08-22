from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.utils.html import strip_tags
from django.contrib import messages
from django.db.models import Q

from .forms import LoginForm, RegisterForm
from .models import Account, AccountManager
from .utils import generate_token
from Arcadia.settings import EMAIL_HOST_USER


account_manager = AccountManager()

class HomePageView(TemplateView):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "home.html", context)


def send_activation_email(request, user, email):

    current_site = get_current_site(request)
    subject = 'Arcadia - Activate your Account'
    context = {'user': user, 'domain': current_site.domain,
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': generate_token.make_token(user)}
    message = render_to_string('activate.html', context)

    plain_message = strip_tags(message)

    send_mail(subject, plain_message, EMAIL_HOST_USER, [email], html_message=message)
    print("Mail Sent")
    

class RegisterView(TemplateView):
    """
        Register View

        Renders registration page, verifies new user.
        On verification sends activation link.
    """

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        fullname = request.POST.get('fullname')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            user = Account.objects.get(Q(username=username) | Q(email=email))
        except Exception as identifier:
            user = None

        if user:
            messages.error(request, 'Username/Email already exists!!')
            return redirect('register')
        if not email.endswith('ahduni.edu.in'):
            messages.error(request, 'Only ahduni emails allowed!!')
            return redirect('register')
        if password1 != password2:
            messages.error(request, 'Passwords didn\'t match!!')
            return redirect('register')

        user = Account(username=username, email=email,
                       fullname=fullname, password=password1)
        user.set_password(password1)
        user.save()

        # Email verification is done by encoding user's primary key and generating a token
        send_activation_email(request, user, email)

        messages.info(request, 'Verification link sent. Check your email! Please wait for 5-7 minutes and check for SPAM/Promotions Folder in Gmail!')
        return redirect('user_login')


class LoginView(TemplateView):
    """
        Login View

        Renders login page and authenticates user.
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
        except Exception as identifier:
            user = None

        if user:
            if not user.is_activated:
                messages.error(request, 'Account not activated.')
                return redirect('user_login')
            login(request, user)
            messages.info(request, 'Logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Username or Password.')
            return redirect('user_login')


class ActivateView(View):
    """
        Email Activation.

        Verification by decoding primary key and checking token
    """

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is None:
            messages.info(request, 'Verification failed!!')
        else:
            if generate_token.check_token(user, token):
                user.is_activated = True
                user.save()
                messages.info(request, 'Link verified successfully!!')
            else:
                messages.info(request, 'Verification failed!!')
        return redirect('user_login')


@login_required
def logout_view(request, *args, **kwargs):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('user_login')


def leaderboard_view(request, *args, **kwargs):
    users = Account.objects.filter(is_superuser=False).order_by('-current_que','last_ans_time')
    context = {'users': users}
    return render(request, 'leaderboard.html', context)


def instruction_view(request, *args, **kwargs):
    context = {}
    return render(request, 'instructions.html', context)
