from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):  #직렬화 (객체 ->json)
    user_name = serializers.ReadOnlyField(source='user_id.username') 

    class Meta:
        model = Review
        fields = ['review_id', 'book_id', 'user_id', 'content', 'rating', 'created_at']
        read_only_fields = ['user_id', 'created_at', 'user_name']
        
    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("1과 5사이의 점수를 입력하세요. ")
        return value