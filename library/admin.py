from django.contrib import admin
from .models import Author, Book, Borrow, Category, Member


# Register your models here.

admin.site.site_header = 'Library Admin'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Category)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'copies', 'is_available']
    list_filter = ['is_available', 'categories']
    search_fields = ['isbn', 'title', 'author_name']
    list_select_related = ['author']
    autocomplete_fields = ['author']

class BorrowInLine(admin.TabularInline):
    model = Borrow
    extra = 0

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'joined_on']
    inlines = [BorrowInLine]

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'borrowed_on', 'due_on', 'returned_on']
    list_filter = ['returned_on']