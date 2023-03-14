from django.contrib.auth.models import User
import uuid  # Requerida para las instancias de libros únicos
from django.db import models
from django.urls import reverse
import uuid  # Requerida para las instancias de libros únicos
from datetime import date


# Create your models here.
'''
class MyModelName(models.Model):
    """
    Una clase típica definiendo un modelo, derivado desde la clase Model.
    """
    # Campos
    my_field_name = models.CharField(max_length=20, help_text='Complete el campo')
    
    # Metadata
    class Meta:
        ordering = ['-my_filed_name']
        
    #   Métodos
    def get_absolute_url(self):
        """
        Devuelve la url para acceder a una instancia particular de MyModelName.
        """
        return reverse("model_detail", args=[str(self.id)])           #kwargs={"pk": self.pk})
    
    def __str__(self):
        """Cadena para representar el objeto MyModelName (en el sitio de Admin, etc.)
        """
        return self.field_name
    
'''


class Genre(models.Model):
    '''Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.).'''
    name = models.CharField(
        max_length=200, help_text='Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.)')

    def __str__(self):
        '''Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)'''
        return self.name

    def get_absolute_url(self):
        '''Retorna la url para acceder a una instancia particular de un autor.'''
        return reverse("genre-detail", kwargs={'pk': self.pk})


class Book(models.Model):
    '''Modelo que representa un libro (pero no un Ejemplar específico).'''
    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.

    summary = models.TextField(
        max_length=1000, help_text='Ingrese una breve descripción del libro')

    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(
        Genre, help_text='Seleccione un género para este libro')
    # ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.
    # La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.
    language = models.ForeignKey('Language', null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['title']    #, 'author']

    def __str__(self):
        '''String que representa al objeto Book'''
        return self.title

    def get_absolute_url(self):
        ''' Devuelve el URL a una instancia particular de Book'''
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'


# Necesario para asignar al usuario como prestatario


class BookInstance(models.Model):
    """
    Modelo que representa una copia específica de un libro (i.e. que puede ser prestado por la biblioteca).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="ID único para este libro particular en toda la biblioteca")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        """Determina si el libro está vencido en función de la fecha de vencimiento y la fecha actual."""
        return bool(self.due_back and date.today() > self.due_back)
    
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m', help_text='Disponibilidad del libro')

    class Meta:
        ordering = ["due_back"]
        permissions = (('can_mark_returned', 'Set book as returned'),)

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.id, self.book.title)


class Author(models.Model):
    ''' Modelo que representa un autor'''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField("born",null=True, blank=True)
    date_of_death = models.DateField("died", null=True, blank=True)

    class Meta:
        ordering = ['last_name']

    def get_absolute_url(self):
        '''Retorna la url para acceder a una instancia particular de un autor.'''
        return reverse("author-detail", kwargs={'pk': self.pk})

    def __str__(self):
        '''String para representar el Objeto Modelo'''
        return '%s, %s' % (self.last_name, self.first_name)


class Language(models.Model):
    name = models.CharField(
        max_length=50, help_text='Introduzca el idioma natural del libro (por ejemplo, inglés, francés, japonés, etc.)".')

    def __str__(self):
        '''Cadena para representar el objeto Modelo (en el sitio Admin, etc.)'''
        return self.name

    def get_absolute_url(self):
        return reverse("language-detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['name']