from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# from authentication.models import User  # 모델에 별도 User가 정의되어 있다면 사용

# User 시리얼라이저(로그인, 로그아웃)(회원가입에 사용도 가능)
class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    def create(self, validated_data):
        # 비밀번호를 해싱하여 저장
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = ['username', 'password']
        # fields = ['username', 'password', 'token']


# 회원가입 시 비밀번호를 해싱하여 저장하는 시리얼라이저
# class RegistrationSerializer(serializers.ModelSerializer):
#     # token = serializers.CharField(max_length=255, read_only=True)
#     password = serializers.CharField(
#         max_length = 128,
#         min_length = 8,
#         write_only = True
#     )

#     class Meta:
#         model = User
#         fields = ['username', 'password']
#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)


#(선택) 응답에 비밀번호 포함 방지
#혹시라도 응답에 password가 포함되지 않도록, to_representation을 오버라이드할 수도 있습니다.