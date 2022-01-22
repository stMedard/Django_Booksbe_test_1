from django.forms import  modelform_factory 
from .models import Book, Chapter
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


AddBookForm = modelform_factory(Book, fields =('title', 'author', 'genre', 'pub_date'))

class ChapterForm(forms.ModelForm):

	class Meta:
		model = Chapter	
		fields =('title_chapter', 'book', 'content')

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)  
		super(ChapterForm, self).__init__(*args, **kwargs)
		self.queryset = Book.objects.filter(user=self.user)
		self.fields["book"].queryset = Book.objects.filter(user=self.user)


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "first_name", "last_name", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


