from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


    class Meta:
        app_label = 'myapp'

    def confirm_email(self):
        self.email_confirmed = True
        self.save()

    def send_confirmation_email(self):
        # Здесь вы можете добавить код для отправки электронного письма с подтверждением
        pass
class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField(upload_to='announcements/images/', blank=True, null=True)
    video = models.FileField(upload_to='announcements/videos/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=[
        ('tank', 'Танки'),
        ('healer', 'Хилы'),
        ('dd', 'ДД'),
        ('merchant', 'Торговцы'),
        ('Gildmasters', 'Гилдмастеры'),
        ('Questgivers', 'Квестгиверы'),
        ('Smiths', 'Кузнецы'),
        ('Leathermen', 'Кожевенники'),
        ('Zelievari', 'Зельевары'),
        ('MastersMagic', 'Мастера заклинаний'),
        # Другие категории объявлений
    ])
    # Другие поля объявления

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    text = models.TextField()

    def send_notification_email(self):
        subject = 'У вас новый отклик на объявление'
        message = f'Здравствуйте, у вас новый отклик на объявление "{self.announcement.title}". Посмотреть отклик можно на сайте.'
        send_mail(subject, message, 'from@example.com', [self.announcement.user.email])

class News(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    # Другие поля новости

class NewsletterSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Другие поля подписки на новостную рассылку

class Verification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)