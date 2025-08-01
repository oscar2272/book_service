from rest_framework import serializers
from . models import Author, Book
from review.serializers import ReviewSerializer

class AuthorSerializer(serializers.ModelSerializer): # 저자 정보
      class Meta:
            model = Author
            fields = ['id', 'name']

class BookListSerializer(serializers.ModelSerializer): #도서 목록 조회
      author_name =  serializers.CharField(source='author.name', read_only=True)
      review_count = serializers.SerializerMethodField()
      average_rating = serializers.SerializerMethodField()
      class Meta:
            model = Book
            fields = ['id', 'title', 'author_name', 'review_count', 'average_rating', 'published_at']
      def get_review_count(self, obj):
            return obj.review_set.count()
      def get_average_rating(self, obj):
            reviews = obj.review_set.all()
            if not reviews.exists():
                    return None
            return round(sum(r.rating for r in reviews) / reviews.count(), 2)

class BookDetailSerializer(serializers.ModelSerializer): #도서 상세 보기
      author = AuthorSerializer(read_only=True)
      reviews = serializers.SerializerMethodField()
      average_rating = serializers.SerializerMethodField()
      review_count = serializers.SerializerMethodField()

      class Meta:
            model = Book
            fields = ['id', 'title', 'author', 'published_at',
                  'average_rating', 'review_count', 'reviews']

      def get_reviews(self, obj):
            reviews_set = obj.review_set.order_by('-created_at')
            return ReviewSerializer(reviews_set, many=True).data

      def get_average_rating(self, obj):
            reviews = obj.review_set.all()
            if not reviews.exists():
                    return None
            return round(sum(r.rating for r in reviews) / reviews.count(), 2)

      def get_review_count(self, obj):
            return obj.review_set.count()

class BookCreateSerializer(serializers.ModelSerializer):
      class Meta:
            model = Book
            fields = ['title', 'author']
      def validate_title(self, value):
            if not value.strip():
                  raise serializers.ValidationError("제목은 공백일 수 없습니다.")
            return value

class BookUpdateSerializer(serializers.ModelSerializer):
      class Meta:
        model = Book
        fields = ['title', 'author']

      def validate_author(self, value):
        if not Author.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("유효하지 않은 저자입니다.")
        return value

class AuthorCreateSerializer(serializers.ModelSerializer):
      class Meta:
            model = Author
            fields = ['name','id']

      def validate_name(self, value):
            if not value.strip():
                  raise serializers.ValidationError("저자 이름은 공백일 수 없습니다.")
            return value