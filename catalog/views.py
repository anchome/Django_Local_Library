from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
import datetime

# from .forms import RenewBookModelForm

# Create your views here.

# Función vista para la página inicio del sitio.


def index(request):
    """Genera contadores de algunos de los objetos principales"""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    """Libros disponibles (status = 'a')"""
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()
    """El 'all()' esta implícito por defecto."""
    num_authors = Author.objects.count()
    num_generos = Genre.objects.count()
    num_languages = Language.objects.count()
    """Numero de visitas a esta view, como está contado en la variable de sesión."""
   

    '''Ejemplo simple de "session" para contar las visitas'''
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_generos': num_generos,
        'num_languages': num_languages,
        'num_visits': num_visits,
    }

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

    """(nuevo nombre para la lista como variable de plantilla, por defecto book_list')"""
    # context_object_name = 'my_book_list'

    """(Consigue 5 libros que contengan el título guerra='war')"""
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='tos')[:5]

    """(Especifique su propio nombre/ubicación de plantilla)"""
    # template_name = 'books/my_arbitrary_template_name_list.html'

    # def get_context_data(self, **kwargs):
    #     """Llama primero a la implementación base para obtener un contexto"""
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     """Obtener el blog de id y añadirlo al contexto"""
    #     context["some_data"] = 'Estos son sólo algunos datos '
    #     return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author


class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 10

class GenreDetailView(generic.DetailView):
    model = Genre


class LanguageListView(generic.ListView):
    model = Language
    paginate_by = 10
    
class LanguageDetailView(generic.DetailView):
    model = Language
    
# listarLibrosPrestadosUsuario
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    '''Vista genérica basada en clases que enumera los libros prestados al usuario actual.'''
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


# listarTodosLibrosPrestados


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Vista genérica basada en clases que lista todos los libros en préstamo. Solo visible para usuarios con permiso can_mark_returned."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')





#   F O R M U L A R I O S


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)

def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Si se trata de una solicitud POST, procese los datos del formulario
    if request.method == 'POST':
        # Crear una instanceancia de formulario y rellenarla con los datos de la solicitud (binding):
        form = RenewBookForm(request.POST)
        # Comprueba si el formulario es válido:
        if form.is_valid():
            # procesar los datos en form.cleaned_data según sea necesario (aquí sólo los escribimos en el campo due_back del modelo)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirigir a una nueva URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # Si es un GET (o cualquier otro método) crea el formulario por defecto.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })
        
    context = {
        'form': form, 
        'bookinstance': book_instance}

    return render(request, 'catalog/book_renew_librarian.html', context )


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(UpdateView):
    model = Book
    fields =['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'

class LanguageCreate(CreateView):
    model = Language
    fields = ['name']
        
class LanguageUpdate(UpdateView):
    model =Language
    fields = ['name',]
    permission_required = 'catalog.can_mark_returned'
    
class LanguageDelete(DeleteView):
    model = Language
    success_url = reverse_lazy('languages')
    permission_required = 'catalog.can_mark_returned'
    
class GenreCreate(CreateView):
    model= Genre
    fields = ['name']
    permission_required = 'catalog.can_mark_returned'
    
class GenreUpdate(UpdateView):
    model = Genre
    fields=['name']
    permission_required = 'catalog.can_mark_returned'
    
class GenreDelete(DeleteView):
    model = Genre
    success_url = reverse_lazy('genres')
    permission_required = 'catalog.can_mark_returned'
