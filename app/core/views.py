from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.middleware.csrf import get_token
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.models import User
from .serializers import UsersSerializer
from django.contrib.auth import authenticate,login, logout
from rest_framework.decorators import api_view, permission_classes
from django.utils.decorators import method_decorator
# 요청 시 CSRF 토큰 반환
@ensure_csrf_cookie
@require_http_methods(["GET"])
def get_csrf_token(request):
    """CSRF 토큰을 반환하는 API"""
    token = get_token(request)
    return JsonResponse({'csrfToken': token})


# 요청 시 로그인

from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny

class UserLoginView(generics.GenericAPIView):
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username:
            return Response({"error": "아이디를 확인하세요."}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({"error": "비밀번호를 확인하세요."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "로그인 성공"}, status=200)
        return Response({"error": "아이디 또는 비밀번호가 올바르지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)



@method_decorator(csrf_exempt, name='dispatch')

# 요청 시 로그아웃(만약, 토큰 기반이면 클라이언트에서 토큰 삭제)
class UserLogoutView(generics.GenericAPIView):
    print("UserLogoutView called")
    # model = User
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        # 로그아웃 로직 구현
        logout(request)
        return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])  # 임시로 허용
def current_user(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "is_admin": user.is_staff or user.is_superuser,
    })