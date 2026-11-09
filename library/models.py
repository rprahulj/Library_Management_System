from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class BookQuerySet(models.QuerySet):
    def available(self):
        return self.filter(is_available=True, copies__gt=0)


class Book(models.Model):
    title = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, unique=True)
    published_year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    copies = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books', blank=True)

    objects = BookQuerySet.as_manager()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='borrow')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrow')
    borrowed_on = models.DateField(default=date.today)
    due_on = models.DateField()
    returned_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.book}->{self.member}'

    @property
    def is_overdue(self):
        return self.returned_on is None and self.due_on < date.today()

    
    