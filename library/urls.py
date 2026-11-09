from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [
path("", RedirectView.as_view(pattern_name="book_list"), name="home"),
path("books/", views.BookListView.as_view(), name="book_list"),
path("books/new/", views.BookCreateView.as_view(), name="book_create"),
path("books/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
path("books/<int:pk>/edit/", views.BookUpdateView.as_view(), name="book_update"),
path("books/<int:pk>/delete/", views.BookDeleteView.as_view(), name="book_delete"),
path("books/<int:pk>/borrow/", views.borrow_book, name="borrow_book"),
path("my_borrow/", views.MyBorrowView.as_view(), name="my_borrow"),
path("borrow/<int:pk>/return/", views.return_borrow, name="return_borrow"),
path("accounts/signup/", views.signup, name="signup"),
]
