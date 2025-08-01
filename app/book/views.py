from rest_framework import generics, permissions
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Book, Author
from .serializers import (
    BookListSerializer,
    BookCreateSerializer,
    BookDetailSerializer,
    BookUpdateSerializer,
    AuthorCreateSerializer
)
from django.db.models import Q,Avg
from django.db.models.functions import Coalesce
from django.db.models import FloatField, Value
from rest_framework import viewsets
class BookPagination(PageNumberPagination):
    page_size = 10

#1. 도서 목록 조회
class BookViewSet(viewsets.ModelViewSet):
    pagination_class = BookPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookCreateSerializer

    def get_queryset(self):
        queryset = Book.objects.annotate(
            avg_rating=Coalesce(Avg('review__rating'), Value(0.0, output_field=FloatField()))
        )
        keyword = self.request.query_params.get('search')
        ordering = self.request.query_params.get('ordering')

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)
            )

        allowed_orderings = ['published_at', 'title', 'author__name', 'avg_rating']
        if ordering:
            order_field = ordering.lstrip('-')
            if order_field in allowed_orderings:
                return queryset.order_by(ordering)

        return queryset.order_by('-published_at')

    def create(self, request, *args, **kwargs):
        print("[BookViewSet] create called with data:", request.data)
        response = super().create(request, *args, **kwargs)
        print("[BookViewSet] create response status:", response.status_code)
        return response

#3. 도서 상세 조회 (nested serializer 사용)
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
    serializer_class = BookDetailSerializer

# 저자 등록,저자 목록 조회
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorCreateSerializer

