from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

# Define a new User admin
class UserAdmin(models.Model):
    email = models.EmailField(max_length = 70, blank = True)
    first_name = models.CharField(max_length = 70, blank = True)
    last_name = models.CharField(max_length = 70, blank = True)
    is_staff = models.BooleanField(
        ('staff status'),
        default=True,
        help_text=('Designates whether the user can log into this admin site.'),
    )
    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

class Genre(models.Model):
    genre = models.CharField(max_length = 200, blank = True)
    
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'
    
    def __str__(self):
        return self.genre

class Book(models.Model):
    pub_date = models.DateField(default = datetime.now, blank = True)
    title = models.CharField(max_length = 200, blank = True, default= '')
    author = models.CharField(max_length = 200, blank = True, default= '')
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, default= '')
    genre = models.ForeignKey(Genre, on_delete = models.CASCADE, help_text = 'Select a genre for this book', null = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class Chapter(models.Model):
    title_chapter = models.CharField(max_length=200, blank=True)
    content = CKEditor5Field('Content', config_name='extends', blank=True)
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, default = '')

    class Meta:
        ordering = ['title_chapter', 'content', 'book']

    def __str__(self):
        return self.title_chapter

    def get_absolute_url(self):
        return reverse('chapter-detail', args=[str(self.id)])



