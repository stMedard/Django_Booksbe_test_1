from django.contrib import admin
from .models import UserAdmin, Book, Chapter, Genre, Illustration
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.auth.models import User


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'id')
    list_filter = ('is_staff', 'is_superuser')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','genre', 'user_b')
    fields = ['title', 'author', 'illustration', 'genre', "user_b"]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
        return qs.filter(user_b=request.user.id)


@admin.register(Illustration)
class IllustrationAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'image')
    fields = ['author_name', 'image']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user.id)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title_chapter', 'book', 'content')
    fields = ['title_chapter', 'book', 'content']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
        return qs.filter(user_c=request.user.id) 

admin.site.register(Genre)


