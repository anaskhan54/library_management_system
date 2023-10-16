from django.urls import path
from api.views import *

urlpatterns=[
    path('books/',book_list),
    path('books/find_books_needed/<int:n>',find_n),
    path('books/unavailable_books',unavailable_books),
    path('book/<int:isbn_no>',book_adv),
    path('book/issue_book/<int:isbn_no>',issue_book),
]