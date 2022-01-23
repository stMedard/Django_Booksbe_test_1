"""django_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from django_rest_app import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
#router.register(r'book', views.BookViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    path('admin/', admin.site.urls, name='admin'),
    path('router/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('accounts/login/', views.login_request, name='login'),
    path('login/', views.login_request, name='login'),
    path('register/', views.register_request, name='register'),
    path("logout/", views.logout_request, name= "logout"),
    
    path('index/', views.PublishedBookListView.as_view(), name='index'),
    path('', views.PublishedBookListView.as_view(), name='index'),
    path('add_book/', views.add_books, name='add_books'),
    path('add_chapter/', views.add_chapter, name='add_chapter'),
    path('edit_chapter/<int:chapter_id>', views.edit_chapter, name='edit_chapter'),
    path('edit_book/<int:book_id>', views.edit_book, name='edit_book'),

    path('books/<int:year>/', views.year_archive),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/', views.UserBookListView.as_view(), name='book-list'),
    path('index/book/<int:pk>/', views.IndexBookDetailView.as_view(), name='book-detail'),

    path('chapter/<int:pk>/', views.ChapterDetailView.as_view(), name='chapter-detail'),
    path('chapters/chapter/<int:pk>/', views.ChapterDetailView.as_view(), name='chapter-detail'),
    path('chapters/', views.ChapterListView.as_view(), name='chapter-list'),
    path('ckeditor/', views.ckeditor5, name='ckeditor5'),
    
] 
urlpatterns += [
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)