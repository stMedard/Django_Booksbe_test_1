#from django.forms import  modelform_factory 
from .models import Book, Chapter, Illustration
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#AddBookForm = modelform_factory(Book, fields =('title', 'author', 'genre', 'publish', 'date_of_publication'))

class IllustrationForm(forms.ModelForm):
	class Meta:
		model = Illustration
		fields = ('author_name', 'image')

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(IllustrationForm, self).__init__(*args, **kwargs)
		#self.fields['image'].widget.clear_checkbox_label = 'clear'
		#self.fields['image'].widget.initial_text = "currently"
		#self.fields['image'].widget.input_text = "change"

from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings

class RelatedFieldWidgetCanAdd(widgets.Select):

    def __init__(self, related_model, related_url=None, *args, **kw):

        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = 'admin:%s_%s_add' % info

        self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
        output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
            (self.related_url, name))
        output.append(u'<img src="%simg/icon-addlink.svg" width="30" height="30" alt="%s"/></a>' % (settings.STATIC_URL, ('Add Another')))                                                                                                                               
        return mark_safe(u''.join(output))

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'genre', 'illustration', 'publish', 'date_of_publication')
        widgets = {
            'publish': forms.RadioSelect,
			'illustration': RelatedFieldWidgetCanAdd(Illustration, related_url="../add_illustration/")
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        print(self.user)
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields["illustration"].queryset = Illustration.objects.filter(user=self.user)

class ChapterForm(forms.ModelForm):

	class Meta:
		model = Chapter	
		fields =('title_chapter', 'book', 'content')
		
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user_b', None) 
		print(self.user) 
		super(ChapterForm, self).__init__(*args, **kwargs)
		self.fields["book"].queryset = Book.objects.filter(user_b=self.user)

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


