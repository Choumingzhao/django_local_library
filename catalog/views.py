from typing import Any
from django.shortcuts import render
from django.views import generic
# Create your views here.
from .models import Book, Author, BookInstance, Genre

# function based view
def index(request):
    """View function for home page of site"""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    num_authors = Author.objects.count()

    num_genres = Genre.objects.count()
    
    num_books_with_word = Book.objects.filter(title__icontains='of').count()
    
    # visit counts
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_with_word': num_books_with_word,
        'num_visits': num_visits
    }
    return render(request, 'index.html', context=context)

# class based view

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5
    context_object_name = 'book_list'
    # queryset = Book.objects.filter(title__icontains='of')[:5]
    template_name = 'book_list.html'
    def get_queryset(self):
        return Book.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['some data'] = 'This is just some data'
        return context
    
class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
    
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5
    context_object_name = 'author_list'
    template_name = 'author_list.html'

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'