from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Announcement, Response, News, NewsletterSubscription, Verification
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AnnouncementForm
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from .forms import ResponseForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            # Имя пользователя уже используется
            return render(request, 'register.html', {'error': 'This username is already taken.'})
        user = User.objects.create_user(username, email, password)

        # Генерация и сохранение кода подтверждения
        verification = Verification.objects.create(user=user)

        # Отправка электронного письма с кодом подтверждения
        subject = 'Подтверждение регистрации'
        message = render_to_string('verification_email.html', {
            'user': user,
            'domain': request.get_host(),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'verification_code': verification.code,
        })
        user.email_user(subject, message)

        return render(request, 'registration_complete.html')
    else:
        return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get('next', '/') # Получаем URL для перенаправления
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next_url) # Перенаправление на URL после входа в систему
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def send_confirmation_email(user_email, confirmation_code):
    # Логика отправки письма с кодом подтверждения регистрации
    pass

def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') # Перенаправление на главную страницу после создания объявления
    else:
        form = AnnouncementForm()
    return render(request, 'create_announcement.html', {'form': form})

def announcement_created(request, announcement_id):
    # Здесь можно добавить логику для отображения страницы с сообщением об успешном создании объявления
    return redirect('announcement_created', announcement_id=new_announcement.id)


def edit_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement_detail', announcement_id=announcement_id)  # Перенаправление на страницу с деталями объявления
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'edit_announcement.html', {'form': form})

@login_required
def user_responses(request, announcement_id):
    user = request.user
    responses = Response.objects.filter(announcement__id=announcement_id)
    # Логика отображения откликов пользователя

@login_required
def response_detail(request, response_id):
    response = get_object_or_404(Response, pk=response_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            response.delete()
            return redirect('user_responses') # Перенаправление на страницу с откликами пользователя
        elif action == 'accept':
            response.status = 'accepted' # Изменение статуса отклика на 'accepted'
            response.save()
            response.send_notification_email() # Отправка уведомления пользователю
            return redirect('user_responses')
    # Логика отображения деталей отклика

@login_required
def accept_response(request, response_id):
    response = get_object_or_404(Response, pk=response_id)
    # Логика принятия отклика и отправки уведомления пользователю

def news_subscription(request):
    if request.method == 'POST':
        # Логика подписки на новостную рассылку
        pass
    else:
        # Отображение формы подписки на новости
        pass

def send_newsletter(news_title, news_text):
    subscribers = NewsletterSubscription.objects.all()
    for subscriber in subscribers:
        send_mail(
            news_title,
            news_text,
            'from@example.com',
            [subscriber.user.email],
            fail_silently=False,
        )

def send_response(request, announcement_id):
    announcement = Announcement.objects.get(pk=announcement_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.announcement = announcement
            response.save()
            response.send_notification_email()  # Отправка уведомления по электронной почте
            return redirect('announcement_detail', announcement_id=announcement_id)  # Перенаправление на страницу с деталями объявления
    else:
        form = ResponseForm()
    return render(request, 'send_response.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Редирект на страницу с сообщением о успешной активации
    else:
        pass

def home_view(request):
    # Здесь вы можете получить все объявления из базы данных и передать их в шаблон
    announcements = Announcement.objects.all()
    return render(request, 'home.html', {'announcements': announcements})
