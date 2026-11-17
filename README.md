# Library Management System

## About the Project

Library Management System is a web application developed using Python and Django.

It helps manage books, authors, categories, library members, and book borrowing activities.

Users can create an account, browse available books, borrow books, and view their borrowing history. The admin can manage books, authors, categories, and borrowing records.

## Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS
- Django ORM

## Features

- User registration and login.
- View all available books.
- Search books by title and author.
- Filter books by category.
- View book details.
- Add, update, and delete books.
- Manage authors and categories.
- Borrow available books.
- Return borrowed books.
- View personal borrowing history.
- Track book availability and copies.
- Automatically create a member account after user registration.
- Django admin panel for library management.

## Project Structure

```text
LibraryManagementSystem/
│
├── library/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── signals.py
│   ├── admin.py
│   └── tests.py
│
├── lms/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── library/
│   └── registration/
│
├── manage.py
└── db.sqlite3
```

## Database Models

The project uses five main models.

1. **Author:** Stores author information.
2. **Category:** Stores book categories.
3. **Book:** Stores book details, price, ISBN, author, and available copies.
4. **Member:** Stores registered library member information.
5. **Borrow:** Stores borrowing and returning details.

## How Book Borrowing Works

1. A user creates an account and logs in.
2. The user selects an available book.
3. The system checks whether copies are available.
4. The system checks whether the user has already borrowed the same book and not returned it.
5. If the book is available, a borrowing record is created.
6. The available book count decreases by one.
7. The user gets 14 days to return the book.
8. When the book is returned, the available copy count increases by one.

The borrowing and returning operations use database transactions to keep book records consistent.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/LibraryManagementSystem.git
```

### 2. Open the Project Folder

```bash
cd LibraryManagementSystem
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

For Windows:

```bash
venv\Scripts\activate
```

### 4. Install Django

```bash
pip install django
```

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create Admin Account

```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```
