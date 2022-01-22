from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from django_rest_app.serializers import UserSerializer, GroupSerializer#, BookSerializer

from .models import Book, Chapter, Book
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .forms import NewUserForm, AddBookForm, ChapterForm
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

#class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows book to be viewed or edited.
    """
#    queryset = Book.objects.all()
#    serializer_class = BookSerializer
#    permission_classes = [permissions.IsAuthenticated]

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
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/index/")
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

def add_books(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html')
    else:
        BookForm = AddBookForm 
        
        if request.method == 'POST':
            formset = BookForm(request.POST)
            
            if formset.is_valid():
                            
                new_book = Book.objects.create(
                    title = formset.cleaned_data["title"],
                    author = formset.cleaned_data["author"],
                    genre = formset.cleaned_data["genre"],
                    pub_date = formset.cleaned_data["pub_date"],
                    user = User.objects.get(username=request.user.username),
                )
                new_book.save()
               
                return redirect('index')
        else:
            formset = BookForm()
           
        return render( request, 'book/add_book.html', {'formset': formset})

class BookDetailView(DetailView):

    model = Book
    template_name = 'book/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs['pk']
        context['chapter_list'] = Chapter.objects.filter(book = book_id)
        return context

class UserBookListView(ListView):

    model = Book
    paginate_by = 100  # if pagination is desired
    template_name = 'book/book_lists.html'
    
    def get_queryset(self):
        return Book.objects.filter(user=self.request.user) 

def add_chapter(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html')
    else:
        
        formset = ChapterForm(user=request.user)
        #print(formset)
        if request.method == 'POST':
            formset = ChapterForm(request.POST, user=request.user)
            print(formset)
            if formset.is_valid():    
                      
                formset.save()
                return redirect('index')
        else:
            formset = ChapterForm(user=request.user)
        
        return render( request, 'book/add_chapter.html', {'formset': formset})

def edit_chapter(request, chapter_id):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html')

    else:
        chapter = Chapter.objects.get(id=chapter_id)
        formset = ChapterForm(user=request.user) 
        
        if request.method == 'POST':
            formset = ChapterForm(instance=chapter, data=request.POST, user=request.user)
            
            if formset.is_valid():
                
                formset.save()
                return redirect('book-list')
        else:
             
            formset = ChapterForm(instance=chapter, user=request.user)
            
        context = {'chapter': chapter, 'BookDetailView': BookDetailView, 'formset': formset}
            
        return render( request, 'book/edit_chapter.html', context)

class ChapterDetailView(DetailView):

    model = Chapter
    template_name = 'book/chapter_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class ChapterListView(ListView):

    model = Chapter
    paginate_by = 20 
    template_name = 'book/chapter_lists.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def ckeditor5(request):
    return render( request, 'book/index.html' )