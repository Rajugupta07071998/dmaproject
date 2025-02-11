from rest_framework import serializers
from .models import PersonalInfo, BusinessInfo, Achievement
from account.models import User

class UserSerializer(serializers.ModelSerializer):
    """Read-only serializer for User model (only for response)"""

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "mobile_number", "user_type"]
        read_only_fields = fields  # Ensure user data is not updated via serializer

class PersonalInfoSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False)
    class Meta:
        model = PersonalInfo
        fields = ["id", "user", "profile_pic", "gender", "location", "bio"]


class PersonalUserInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested User serializer
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = PersonalInfo
        fields = ["id", "user", "profile_pic", "gender", "location", "bio"]


class BusinessInfoSerializer(serializers.ModelSerializer):
    business_logo = serializers.ImageField(required=False)
    class Meta:
        model = BusinessInfo
        fields = '__all__'


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'
        read_only_fields = ['business']
