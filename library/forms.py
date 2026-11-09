from django import forms
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'published_year', 'price', 'copies', 'author', 'categories']
        Widgets = {'categories' : forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.setdefault('class', 'form-control')

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0 :
            raise forms.ValidationError('Price must be greater than zero')
        return price

    def clean_published_year(self):
        published_year = self.cleaned_data['published_year']
        if published_year > date.today().year:
            raise forms.ValidationError('Publish year can not be in future')
        return published_year


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
