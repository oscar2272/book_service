from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.middleware.csrf import get_token
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.models import User
from .serializers import UsersSerializer, RegistrationSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

# 요청 시 CSRF 토큰 반환
@ensure_csrf_cookie
@require_http_methods(["GET"])
def get_csrf_token(request):
    """CSRF 토큰을 반환하는 API"""
    token = get_token(request)
    return JsonResponse({'csrfToken': token})


#모든 API에 @csrf_exempt가 적용되어 있습니다.
#REST API라면 괜찮지만, 보안상 주의가 필요합니다.
# 요청 시 로그인
@csrf_exempt  # CSRF 보호를 비활성화하기 위한 데코레이터이나, REST API라면 필요에 따라 제거 가능
class UserLoginView(generics.GenericAPIView):
    # model = User # generics.GenericAPIView에서 model은 필수가 아님
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        # 로그인 로직 구현
        if not username:
            return Response({"error": "아이디를 확인하세요."}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({"error": "비밀번호를 확인하세요."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        # authenticate 함수는 사용자 인증을 수행합니다. # 성공하면 User 객체를 반환하고, 실패하면 None을 반환합니다.
        # 실제 로그인 처리는 authenticate 함수로 수행됩니다.# authenticate 함수는 기본적으로 User 모델을 사용합니다.

        # 만약 커스텀 User 모델을 사용한다면, 해당 모델을 import하고 authenticate 함수에 해당 모델을 사용하도록 설정해야 합니다.
        # 예: from authentication.models import User
        # user = authenticate(username=username, password=password, user_model=User)
        if user is not None:
            login(request, user)
            # 만약, 토큰 발급이 필요하다면 여기서 발급 (예: SimpleJWT 등)
            return Response({"message": "로그인에 성공하였습니다."}, status=status.HTTP_200_OK)
        return Response({"error": "아이디 또는 비밀번호가 올바르지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)


# 요청 시 로그아웃(만약, 토큰 기반이면 클라이언트에서 토큰 삭제)
@csrf_exempt
class UserLogoutView(generics.GenericAPIView):
    # model = User
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        # 로그아웃 로직 구현
        logout(request)
        return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)


# 요청 시 회원가입
# @csrf_exempt
# class RegistrationAPIView(generics.GenericAPIView):
#     serializer_class = RegistrationSerializer
#     permission_classes = [AllowAny]
    
#     def post(self, request):
#         # 유효성 검사 통과 후 사용자 생성
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "회원가입이 되었습니다."}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# models.py 에 별도의 User 모델을 정의하여 사용한다면, 해당 모델을 import하여 사용해야 합니다.
# from authentication.models import User 
# 유저 조회 + 생성
# class Userlist(generics.ListCreateAPIView): # ← 단일 클래스로 축약
#     queryset = Users.objects.all()
#     serializer_class = UsersSerializer

# # 단일 조회 + 수정 + 삭제
# class Userdetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Users.objects.all()
#     serializer_class = UsersSerializer