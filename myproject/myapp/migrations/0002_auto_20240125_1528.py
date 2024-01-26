# Generated by Django 3.2.23 on 2024-01-25 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='announcements/images/'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='announcements/videos/'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='category',
            field=models.CharField(choices=[('tank', 'Танки'), ('healer', 'Хилы'), ('dd', 'ДД'), ('merchant', 'Торговцы'), ('Gildmasters', 'Гилдмастеры'), ('Questgivers', 'Квестгиверы'), ('Smiths', 'Кузнецы'), ('Leathermen', 'Кожевенники'), ('Zelievari', 'Зельевары'), ('MastersMagic', 'Мастера заклинаний')], max_length=50),
        ),
    ]
