from rest_framework import serializers
from .models import PersonalInfo, BusinessInfo, Achievement, Notification, BusinessMembership, MembershipRequest, EquipmentMaster, UserActivity
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



class MembershipRequestSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name', read_only=True)
    business = serializers.CharField(source='business.business_name', read_only=True)

    class Meta:
        model = MembershipRequest
        fields = ['id', 'user', 'business', 'status', 'created_at']


class BusinessMembershipSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name', read_only=True)
    business = serializers.CharField(source='business.business_name', read_only=True)

    class Meta:
        model = BusinessMembership
        fields = ['id', 'user', 'business', 'joined_at']



class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'
        read_only_fields = ['business']




class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'sender', 'notification_type', 'message', 'is_read', 'created_at']




class EquipmentMasterSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)  

    class Meta:
        model = EquipmentMaster
        fields = '__all__'




# Business Members List Serializer
class BusinessMemberSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user.id', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    joined_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    #user = UserSerializer(read_only=True)
    personal_info = PersonalInfoSerializer(source='user.personalinfo', read_only=True) 

    class Meta:
        model = BusinessMembership
        fields = ['user_id', 'user_name', 'joined_at', 'personal_info']


# User Details Serializer by click user from list of user
class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    joined_businesses = serializers.SerializerMethodField()
    personal_info = PersonalInfoSerializer(source='user.personalinfo', read_only=True)  

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'mobile_number', 'user_type', 'personal_info', 'joined_businesses']

    def get_joined_businesses(self, obj):
        """Fetches the list of businesses the user has joined"""
        return [
            {
                "business_id": membership.business.id,
                "business_name": membership.business.business_name
            }
            for membership in obj.business_memberships.all()
        ]
    

class UserFullDataSerializer(serializers.ModelSerializer):
    personal_info = PersonalInfoSerializer(source='personalinfo', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'mobile_number', 'user_type', 'master_policy', 
                  'batch_policy', 'first_name', 'last_name', 'username', 'personal_info']
        


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'  # Include all fields