from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from django_rest_app.serializers import UserSerializer, GroupSerializer#, BookSerializer

from .models import Book, Chapter, Book, Illustration
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .forms import NewUserForm, BookForm, ChapterForm, IllustrationForm


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
        formset = Form(user=request.user)
        
        if request.method == 'POST':
            formset = Form(request.POST, user=request.user)
            
            if formset.is_valid():
                    
                new_book = Book.objects.create(
                    title = formset.cleaned_data["title"],
                    author = formset.cleaned_data["author"],
                    genre = formset.cleaned_data["genre"],
                    illustration = formset.cleaned_data["illustration"],
                    publish = formset.cleaned_data["publish"],
                    date_of_publication = formset.cleaned_data["date_of_publication"],
                    user_b = User.objects.get(username=request.user.username),
                )
                new_book.save()
                #formset.save()
                return redirect('book-list')
        else:
            
            formset = Form(user=request.user)
            
           
        return render( request, 'book/add_book.html', {'formset': formset})
    
def edit_book(request, book_id):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html')

    else:
        book = Book.objects.get(id=book_id)
        formset = BookForm(book, user=request.user) 
        
        if request.method == 'POST':
            formset = BookForm(instance=book, data=request.POST, user=request.user)
            
            if formset.is_valid():
                
                formset.save()
                return redirect('book-list')
        else:
             
            formset = BookForm(instance=book, user=request.user)
            
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
        return Book.objects.filter(user_b=self.request.user) 

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
        
        formset = ChapterForm(user_b=request.user)

        if request.method == 'POST':
            formset = ChapterForm(request.POST, user_b=request.user)

            if formset.is_valid():    
                new_chapter = Chapter.objects.create(
                    title_chapter = formset.cleaned_data["title_chapter"],
                    content = formset.cleaned_data["content"],
                    book = formset.cleaned_data["book"],
                    user_c = User.objects.get(username=request.user.username),
                    
                )
                new_chapter.save() 
                return redirect('book-list')
        else:
            formset = ChapterForm(user_b=request.user)
        
        return render( request, 'book/add_chapter.html', {'formset': formset})

def add_illustration(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html')
    else:
        
        formset = IllustrationForm(user=request.user)

        if request.method == 'POST':
            formset = IllustrationForm(request.POST, request.FILES, user=request.user)

            if formset.is_valid():    
                new_illustration = Illustration.objects.create(
                    author_name = formset.cleaned_data["author_name"],
                    image = formset.cleaned_data["image"],
                    user = User.objects.get(username=request.user.username),
                    
                )
                new_illustration.save()  
            
                return redirect('book-list')
        else:
            formset = IllustrationForm(user=request.user)
        
        return render( request, 'book/add_illustration.html', {'formset': formset})

def edit_chapter(request, chapter_id):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html')

    else:
        chapter = Chapter.objects.get(id=chapter_id)
        formset = ChapterForm(user_b=request.user) 
        
        if request.method == 'POST':
            formset = ChapterForm(instance=chapter, data=request.POST, user_b=request.user)
            
            if formset.is_valid():
                
                formset.save()
                return redirect('book-list')
        else:
             
            formset = ChapterForm(instance=chapter, user_b=request.user)
            
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

from reportlab.platypus import Paragraph, Spacer, PageBreak, BaseDocTemplate,PageTemplate, Frame , NextPageTemplate, Image
from reportlab.rl_config import defaultPageSize
from django.http import HttpResponse
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm, inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont  
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

class MyDocTemplate(BaseDocTemplate):
    
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            E = [0, text, self.page]
            bn = getattr(flowable,'_bookmarkName',None)
            if bn is not None: 
                E.append(bn), 
                self.notify('TOCEntry', tuple(E))
            else:
                return

def generatePDF(request, id):
    Frame1=Frame(2.5*cm, 2.3*cm, 16*cm, 25*cm,id='F1')
    PAGE_HEIGHT=defaultPageSize[1]
    PAGE_WIDTH=defaultPageSize[0]
    
    top_margin = A4[1] - inch
    bottom_margin = inch
    left_margin = inch
    right_margin = A4[0] - inch

    book = Book.objects.get(id=id)
    Title = book.title
    Author = book.author
    pageinfo = "%s / %s " % (Author, Title)
    file_name = book.title
    doc = MyDocTemplate(file_name)
    chapters = Chapter.objects.filter(book_id = id)
    

    def drawPageFrame(canv):
        canv.line(left_margin, top_margin, right_margin, top_margin)
        canv.setFont('Berylium',9)
        canv.drawString(left_margin, top_margin + 2, pageinfo)
        canv.line(left_margin, top_margin, right_margin, top_margin)
        canv.line(left_margin, bottom_margin, right_margin, bottom_margin)
        canv.drawCentredString(0.5*A4[0], 0.5 * inch,"Page %d" % canv.getPageNumber())

    def myFirstPage(canvas, doc):
        canvas.saveState()
        canvas.setFont('BeryliumBd',18)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-190, Title)
        canvas.setFont('BeryliumIt',14)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-210, Author)
        canvas.setFont('Berylium',9)
        canvas.drawString(inch, 0.75 * inch, " ")
        canvas.restoreState()
            
    def myLaterPages(canvas, doc):
        
        #page_num = canvas.getPageNumber()
        #key = 'ch%s' % doc.seq.nextf('style0')
        #canvas.bookmarkPage(key)
        #doc.notify('TOCEntry', (0, 'Chapter 1', page_num, key))
        #canvas.saveState()
        canvas.setAuthor(book.author)
        canvas.setTitle(book.title)
        canvas.setSubject("BooksBe")           
        drawPageFrame(canvas)
    
    def go():
        pdfmetrics.registerFont(TTFont('Berylium', 'resources/fonts/Berylium/Berylium.ttf'))
        pdfmetrics.registerFont(TTFont('BeryliumBd', './resources/fonts/Berylium/Beryliumbold.ttf'))
        pdfmetrics.registerFont(TTFont('BeryliumIt', './resources/fonts/Berylium/BeryliumItalic.ttf'))
        pdfmetrics.registerFont(TTFont('BeryliumBI', './resources/fonts/Berylium/BeryliumboldItalic.ttf'))
        registerFontFamily('Berylium', normal='Berylium', bold='BeryliumBd', italic='BeryliumIt', boldItalic='BeryliumBI')

        Story = []  

        style0 = ParagraphStyle('style0',
                                alignment=TA_LEFT,
                                fontName='BeryliumBd',
                                fontSize=12) 
        style1 = ParagraphStyle('style1',
                                alignment=TA_CENTER,
                                fontName='BeryliumBd',
                                leading = 14,
                                fontSize=14)
        style2 = ParagraphStyle('style2',
                                alignment=TA_JUSTIFY,
                                fontName='Berylium',
                                leading = 14,
                                fontSize=11)
        doc.addPageTemplates([PageTemplate(id='TitlePage', frames=Frame1, onPage=myFirstPage),PageTemplate(id='ContentPage', frames=Frame1, onPage=myLaterPages)])

        Story.append(NextPageTemplate('TitlePage'))
        filename = book.illustration.image
        Story.append(Spacer(2,4*inch))
        Story.append(Image(filename, width=15*cm,height=11*cm))
        Story.append(NextPageTemplate('ContentPage'))
        Story.append(PageBreak())
        Story.append(Spacer(2,1*inch))
        Story.append(Paragraph("""Table of Contents:""", style1))
        Story.append(Spacer(1,0.3*inch))
        toc = TableOfContents() 
        toc.levelStyles = [style0, style1, style2]        
        Story.append(toc)
        Story.append(PageBreak())

        def doHeading(text,sty):
            from hashlib import sha1
            bn=sha1((text+sty.name).encode('utf8')).hexdigest()
            h=Paragraph(text+'<a name="%s"/>' % bn, sty)
            h._bookmarkName=bn
            Story.append(h) 
        chapterNum = 0
        for i in chapters:        
            Story.append(NextPageTemplate('ContentPage'))    
            doc.multiBuild(Story)
            chapterNum += 1
            Story.append(Spacer(2,1*inch))
            Story.append(Paragraph("Chapter " + str(chapterNum), style1))
            Story.append(Spacer(2,0.2*inch))
            d = (" %s" % i.title_chapter  )
            doHeading(d, style1)
            Story.append(Spacer(2,1*inch))
            e = (" %s" % i.content )
            str(e).replace('\n','<br />\n')
            g = Paragraph(e, style2)
            Story.append(g)
            Story.append(PageBreak())
            doc.multiBuild(Story)



    try:
        chapters[0] is None
    except:
        return redirect("/add_chapter")

    if book.illustration is None:
        return redirect('/edit_book/'+ str(book.id))
    else:
       go() 
    
    return HttpResponse(open(book.title, 'br'), content_type='application/pdf')    


