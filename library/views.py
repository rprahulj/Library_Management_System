from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView

from .forms import BookForm, SignUpForm
from .models import Book, Category, Borrow



# Create your views here.
class BookListView(ListView):
    model = Book
    paginate_by = 6
    context_object_name = "books"

    def get_queryset(self):
        qs = Book.objects.select_related("author").prefetch_related("categories")
        q = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(author__name__icontains=q))
        if category:
            qs = qs.filter(categories__pk=category)
        return qs.distinct()
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["categories"] = Category.objects.all()
        return ctx


class BookDetailView(DetailView):
    queryset = Book.objects.select_related("author").prefetch_related("categories")
    context_object_name = "book"


class BookCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "library.add_book"
    model = Book
    form_class = BookForm


class BookUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "library.change_book"
    model = Book
    form_class = BookForm


class BookDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "library.delete_book"
    model = Book
    success_url = reverse_lazy("book_list")



@login_required
@require_POST
def borrow_book(request, pk):
    with transaction.atomic():
        book = get_object_or_404(Book.objects.select_for_update(), pk=pk)
        member = request.user.member
        if not book.is_available or book.copies < 1:
            messages.error(request, f"'{book.title}' is not available right now.")
        elif Borrow.objects.filter(book=book, member=member, returned_on__isnull=True).exists():
            messages.warning(request, "You already have this book.")
        else:
            Borrow.objects.create(book=book, member=member, due_on=date.today() + timedelta(days=14))
            book.copies -= 1
            book.is_available = book.copies > 0
            book.save(update_fields=["copies", "is_available"])
            messages.success(request, f"You borrowed '{book.title}'. Please return it within 14 days.")
    return redirect("book_detail", pk=pk)



@login_required
@require_POST
def return_borrow(request, pk):
    with transaction.atomic():
        borrow = get_object_or_404(Borrow, pk=pk, member__user=request.user, returned_on__isnull=True)
        borrow.returned_on = date.today()
        borrow.save(update_fields=["returned_on"])
        book = borrow.book
        book.copies += 1
        book.is_available = True
        book.save(update_fields=["copies", "is_available"])
    messages.success(request, f"Thanks! '{book.title}' has been returned.")
    return redirect("my_borrow")



class MyBorrowView(LoginRequiredMixin, ListView):
    template_name = "library/my_borrow.html"
    context_object_name = "borrow"
    def get_queryset(self):
        return (Borrow.objects.filter(member__user=self.request.user)
            .select_related("book__author")
            .order_by("returned_on", "due_on"))


def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save() # signal creates the Member
        login(request, user)
        messages.success(request, "Welcome! Your account has been created.")
        return redirect("book_list")
    return render(request, "registration/signup.html", {"form": form})