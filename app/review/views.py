from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly



class ReviewListCreate(generics.ListCreateAPIView): #리뷰 목록 전체 조회, 생성
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # 로그인 안한 사용자는 조회만 가능

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class ReviewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView): #리뷰 수정, 삭제
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def put(self, request, *args, **kwargs):
        print("[DEBUG] PUT request data:", request.data)
        return super().put(request, *args, **kwargs)
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]