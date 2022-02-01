from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
#from django_ckeditor_5.fields import CKEditor5Field
from ckeditor.fields import RichTextField

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

class Illustration(models.Model):

    author_name = models.CharField(max_length = 200, blank = True, default= '')
    image = models.ImageField(upload_to ='uploads/', null=True, blank=True)#height_field=400, width_field=600,
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, default= '')
    
    def get_absolute_url(self):
        return reverse('add_illustration', args=[str(self.id)])

class Book(models.Model):
    date_of_publication = models.DateField(default = datetime.now, blank = True)
    title = models.CharField(max_length = 200, blank = True, default= '')
    author = models.CharField(max_length = 200, blank = True, default= '')
    illustration = models.ForeignKey(Illustration, on_delete = models.CASCADE, null = True, blank = True)
    user_b = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, default = '')
    genre = models.ForeignKey(Genre, on_delete = models.CASCADE, null = True)
    CHOICES = ((True, 'Yes'), (False, 'No'))
    publish = models.BooleanField(default = False, choices = CHOICES, help_text = 'Just how the book is going to be published now')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class Chapter(models.Model):
    title_chapter = models.CharField(max_length=200, blank=True)
    content = RichTextField()
    #content = CKEditor5Field('Content', config_name='extends', blank=True)
    user_c = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, default = '')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, default = '')

    class Meta:
        ordering = ['title_chapter', 'content', 'book']

    #def __str__(self):
    #    return self.title_chapter
    
    def get_absolute_url(self):
        return reverse('chapter-detail', args=[str(self.id)])



