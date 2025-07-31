from rest_framework import generics, permissions, filters
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Book
from .serializers import (
    BookListSerializer,
    BookCreateSerializer,
    BookDetailSerializer,
    BookUpdateSerializer
)

class BookPagination(PageNumberPagination):
    page_size = 10
    
#1. 도서 목록 조회
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    pagination_class = BookPagination
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'author__name']  
    ordering_fields = ['published_at']  
    ordering = ['average_rating','published_at']  
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering')

        if not ordering:
            return queryset.order_by('-published_at')
        
        return queryset

#2. 도서 등록
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

#3. 도서 상세 조회
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [permissions.AllowAny]

#4. 도서 수정
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

#5. 도서 삭제
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated]