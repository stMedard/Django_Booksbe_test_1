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

from .forms import NewUserForm, BookForm, ChapterForm
#from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.decorators import login_required



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
			return redirect("/index/")
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
        Form = BookForm 
        
        if request.method == 'POST':
            formset = Form(request.POST)
            
            if formset.is_valid():
                            
                new_book = Book.objects.create(
                    title = formset.cleaned_data["title"],
                    author = formset.cleaned_data["author"],
                    genre = formset.cleaned_data["genre"],
                    publish = formset.cleaned_data["publish"],
                    date_of_publication = formset.cleaned_data["date_of_publication"],
                    user = User.objects.get(username=request.user.username),
                )
                new_book.save()
               
                return redirect('book-list')
        else:
            formset = Form()
           
        return render( request, 'book/add_book.html', {'formset': formset})
    
def edit_book(request, book_id):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html')

    else:
        book = Book.objects.get(id=book_id)
        formset = BookForm(book) 
        
        if request.method == 'POST':
            formset = BookForm(instance=book, data=request.POST)
            
            if formset.is_valid():
                
                formset.save()
                return redirect('book-list')
        else:
             
            formset = BookForm(instance=book)
            
        context = {'book': book, 'BookDetailView': BookDetailView, 'formset': formset}
            
        return render( request, 'book/edit_book.html', context)

class BookDetailView(DetailView):

    model = Book
    template_name = 'book/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs['pk']
        context['chapter_list'] = Chapter.objects.filter(book = book_id)
        return context

class IndexBookDetailView(DetailView):

    model = Book
    template_name = 'book/index_book_detail.html'

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

class PublishedBookListView(ListView):

    model = Book
    paginate_by = 100  # if pagination is desired
    template_name = 'index.html'
    
    def get_queryset(self, *args, **kwargs):
        return Book.objects.filter(publish=True) 

def add_chapter(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html')
    else:
        
        formset = ChapterForm(user=request.user)

        if request.method == 'POST':
            formset = ChapterForm(request.POST, user=request.user)
            print(formset)
            if formset.is_valid():    
                      
                formset.save()
                return redirect('book-list')
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

from django.http import FileResponse
#from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
#from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
#from django.http import HttpResponse, HttpResponseBadRequest
#from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont  
#from reportlab.lib.pagesizes import letter, A5
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
PAGESIZE = (140 * mm, 216 * mm)
BASE_MARGIN = 5 * mm

def generatePDF(request,id):
    pdfmetrics.registerFont(TTFont('Berylium', 'resources/fonts/Berylium/Berylium.ttf'))
    pdfmetrics.registerFont(TTFont('BeryliumBd', './resources/fonts/Berylium/Beryliumbold.ttf'))
    pdfmetrics.registerFont(TTFont('BeryliumIt', './resources/fonts/Berylium/BeryliumItalic.ttf'))
    pdfmetrics.registerFont(TTFont('BeryliumBI', './resources/fonts/Berylium/BeryliumboldItalic.ttf'))
    registerFontFamily('Berylium', normal='Berylium', bold='BeryliumBd', italic='BeryliumIt', boldItalic='BeryliumBI')
    PAGE_HEIGHT=defaultPageSize[1]
    PAGE_WIDTH=defaultPageSize[0]
    book = Book.objects.get(id=id)
    Title = book.title
    pageinfo = book.title
    Author = book.author
    Filename = book.title

    def myFirstPage(canvas, doc):
        canvas.saveState()
        canvas.setFont('BeryliumBd',18)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-130, Title)
        canvas.setFont('BeryliumIt',14)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-160, Author)
        canvas.setFont('Berylium',9)
        canvas.drawString(inch, 0.75 * inch,"First Page / %s" % pageinfo)
        canvas.restoreState()
        canvas.showPage()
    
    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Berylium', 9)
        canvas.drawString(inch, 0.75 * inch,"Page %d %s" % (doc.page, pageinfo))
        canvas.restoreState()
    
    def go():

        doc = SimpleDocTemplate(filename=Filename, title=book.title, author=book.author)   
        Story = [Spacer(2,2*inch)]
        style1 = ParagraphStyle('BeryliumBd',
                                alignment=TA_CENTER,
                                fontName='BeryliumBd',
                                fontSize=14)
        style2 = ParagraphStyle('Berylium',
                                alignment=TA_JUSTIFY,
                                fontName='Berylium',
                                fontSize=11)

        chapters = Chapter.objects.filter(book_id = id)

        for i in chapters:
         
            d = (" %s" % i.title_chapter )
            f = Paragraph(d, style1)
            Story.append(Spacer(2,1*inch))
            Story.append(f)
            Story.append(Spacer(2,1*inch))
            e = (" %s" % i.content )
            g = Paragraph(e, style2)
            Story.append(g)
            Story.append(Spacer(2,2*inch))
            Story.append(PageBreak())

        doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)    

    go()
    return FileResponse(open(Filename, 'br'), content_type='application/pdf')    

