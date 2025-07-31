from django.urls import path
from .views import (BookListView, BookCreateView, BookDetailView,BookUpdateView, BookDeleteView
)# 혹은 from book import views


urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('', BookCreateView.as_view(), name='book-create'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]