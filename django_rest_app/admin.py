from django.contrib import admin
from .models import UserAdmin, Book, Chapter, Genre
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
    list_display = ('title', 'author', 'genre', 'user')
    fields = ['title', 'author', 'genre', "user"]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user.id)

#admin.site.register(Author)
#admin.site.register(Book)
#admin.site.register(Chapter)
admin.site.register(Genre)
admin.site.register(Chapter)
# Register your models here.
