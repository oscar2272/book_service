from django.urls import path
from .views import (

  BookDetailView,
  BookUpdateView,
  BookDeleteView,
  BookViewSet
)# 혹은 from book import views


urlpatterns = [
    path('', BookViewSet.as_view(({'get': 'list', 'post': 'create'})), name='book-list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]