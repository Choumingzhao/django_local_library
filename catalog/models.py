import uuid

from django.db import models
from django.urls import reverse # used in get_absolute_url() to get URL for specific id

from django.db.models import UniqueConstraint # Constrain fields to unique values
from django.db.models.functions import Lower # Return lower cased value of field

class Genre(models.Model):
    """Model reprsenting a book genre."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text='Enter a book genre (e.g. Science Fiction, French Poetry etc.)',
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        """Return the url to accesss a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genra_name_case_insensitive_unique',
                violation_error_message='Genre with this name already exists '
                    '(case insensitive match).',
            ),
        ]

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.RESTRICT, null=True)
    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book.'
    )
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a '
                            'href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.RESTRICT, null=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        """Return the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    """Model represeing a specific copy of a bookk (i.e. that can be borrowed 
    from the libarary)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = ( 
       ('m', 'Maintainance'), 
       ('o', 'On loan'),
       ('a', 'Available'),
       ('r', 'Reserved'),
     )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self) -> str:
        return f"{self.id} ({self.book.title})"


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular Author: Firstname Lastname."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self) -> str:
        return f'{self.last_name}, {self.first_name}'
    

class Language(models.Model):
    """Model representing a language of a book."""
    name = models.CharField(
        max_length=200,
        help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)"
    )
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message='Language with this name already exists '
                    '(case insensitive match).',
            ),
        ]
        
    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self) -> str:
        return self.name