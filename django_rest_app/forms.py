
from django.forms import ModelForm, TextInput, Textarea, ChoiceField, DateField, modelform_factory 
from .models import Book, Chapter
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

AddBookForm = modelform_factory(Book, fields =('__all__'))

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


