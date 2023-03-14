from django.contrib import admin
from .models import Author, Book, Genre, BookInstance, Language

# Register your models here.
"""Registro mínimo de los modelos
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookInstance)   
admin.site.register(Genre)
admin.site.register(Language)
"""

admin.site.register(Genre)
admin.site.register(Language)

class BooksInline(admin.TabularInline):
    """Define el formato de inserción de libros en línea (utilizado en AuthorAdmin"""
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]


class BookInstanceInline(admin.TabularInline):
    """Define el formato de inserción de instancias de libros en línea (utilizado en BookAdmin)"""
    model = BookInstance



class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]
    
admin.site.register(Book, BookAdmin)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status','borrower','due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            "fields": (
                'book',
                'imprint',
                'id'
            ),
        }),
        ('Disponibilidad',{
            'fields':(
                'status',
                'due_back',
                'borrower',
            )
        }),
    )
    