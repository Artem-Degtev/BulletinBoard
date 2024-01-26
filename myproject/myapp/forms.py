from django import forms
from .models import Announcement, Response

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['user', 'title', 'text', 'category']  # Замените на реальные поля вашей модели Announcement

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']