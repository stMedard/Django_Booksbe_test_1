from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from django_rest_app.serializers import UserSerializer, GroupSerializer, BookSerializer

from .models import Book, Chapter, Book, Genre
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.forms import modelform_factory
from .forms import AddBookForm
from .forms import NewUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows book to be viewed or edited.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_staff = True
			user = form.save()
			my_group = Group.objects.get(name='Author') 
			my_group.user_set.add(user)
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/admin/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="accounts/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		print('raz')
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			print('dwa')
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				print('trzy')
				return redirect("/admin/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="accounts/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("index")

def index( request):

    return render(request, 'index.html')

def year_archive(request, year):
    b_list = Book.objects.filter(pub_date__year=year)
    context = {'year': year, 'book_list': b_list}
    return render(request, 'book/year_archive.html', context)

def add_books( request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html')
    else:
        BookForm1 = AddBookForm 
        
        print("jeden")
        if request.method == 'POST':
            formset = BookForm1(request.POST)
            print(request.POST)
            
            if formset.is_valid():
                stock = formset.save(commit=False)
                stock.save()
                print("dwa")
                return redirect('index')
                
        else:
            formset = BookForm1()
        return render( request, 'book/add_book.html', {'formset': formset})

class BookDetailView(DetailView):

    model = Book
    template_name = 'book/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs['pk']
        context['chapter_list'] = Chapter.objects.filter(book = book_id)
        return context

class BookListView(ListView):

    model = Book
    paginate_by = 100  # if pagination is desired
    template_name = 'book/book_lists.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ChapterDetailView(DetailView):

    model = Chapter
    template_name = 'book/chapter_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #chapter_id = self.kwargs['pk']
        #context['book_detail'] = Book.objects.filter(title = chapter_id)
        #context['genre_detail'] = Genre.objects.filter(genre = chapter_id)

        return context

class ChapterListView(ListView):

    model = Chapter
    paginate_by = 20 
    template_name = 'book/chapter_lists.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context