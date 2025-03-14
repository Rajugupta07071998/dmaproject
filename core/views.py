from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PersonalInfo, BusinessInfo, Achievement, BusinessMembership, MembershipRequest
from .serializers import *
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated




def update_user_fields(user, data):
    """Helper function to update User model fields manually"""
    user_fields = ["first_name", "last_name", "email", "mobile_number", "user_type"]
    
    updated = False  # Track if any field is updated

    for field in user_fields:
        value = data.get(field, "").strip()
        if value and getattr(user, field) != value:  # Check if value exists and is different
            setattr(user, field, value)
            updated = True  # Mark update required

    if updated:
        user.save()


# Personal Info APIs using ID
class PersonalInfoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        """Retrieve user's personal info by ID"""
        try:
            personal_info = PersonalInfo.objects.get(id=pk)
            serializer = PersonalUserInfoSerializer(personal_info)
            return Response(serializer.data)
        except PersonalInfo.DoesNotExist:
            return Response({"error": "Personal Info not found"}, status=404)

    def post(self, request):
        """Create personal info for a user and update User model fields"""
        if PersonalInfo.objects.filter(user=request.user).exists():
            return Response({"error": "Personal Info already exists"}, status=400)
        
        # Add the user to the request data manually(Frontend share)
        request.data['user'] = request.user.id  # Assign the current logged-in user

        serializer = PersonalInfoSerializer(data=request.data)
        if serializer.is_valid():
            personal_info = serializer.save()

            # **User table update logic (Manually updating fields)**
            user = request.user
            update_user_fields(user, request.data)  # Function to update user fields

            return Response(
                {"message": "Personal Info created successfully", "data": PersonalUserInfoSerializer(personal_info).data},
                status=201
            )
        return Response(serializer.errors, status=400)

    def patch(self, request, pk=None):
        """Partial update personal info by ID and update User model fields"""
        try:
            personal_info = PersonalInfo.objects.get(id=pk)

            # **Check if the user is the owner of this PersonalInfo**
            if personal_info.user != request.user:
                return Response({"error": "You are not allowed to update this information"}, status=403)

            serializer = PersonalInfoSerializer(personal_info, data=request.data, partial=True)
            if serializer.is_valid():
                personal_info = serializer.save()

                # **User table update logic (Manually updating fields)**
                user = request.user
                update_user_fields(user, request.data)  # Function to update user fields

                return Response(
                    {"message": "Personal Info updated successfully", "data": PersonalUserInfoSerializer(personal_info).data},
                    status=200
                )
            return Response(serializer.errors, status=400)
        except PersonalInfo.DoesNotExist:
            return Response({"error": "Personal Info not found"}, status=404)

    # def delete(self, request, pk=None):
    #     """Delete personal info by ID"""
    #     try:
    #         personal_info = PersonalInfo.objects.get(id=pk, user=request.user)
    #         personal_info.delete()
    #         return Response({"message": "Personal Info deleted successfully"})
    #     except PersonalInfo.DoesNotExist:
    #         return Response({"error": "Personal Info not found"}, status=404)


# Business Info APIs using ID
class BusinessInfoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        """Retrieve business info by ID"""
        try:
            if request.user.user_type != 'business':
                return Response({"error": "You are not Business User"}, status=400)
            
        
            business_info = BusinessInfo.objects.get(id=pk)
            serializer = BusinessInfoSerializer(business_info)
            return Response(serializer.data)
        except BusinessInfo.DoesNotExist:
            return Response({"error": "Business Info not found"}, status=404)

    def post(self, request):
        """Create business info for a user"""
        if BusinessInfo.objects.filter(user=request.user).exists():
            return Response({"error": "Business Info already exists"}, status=400)
        
        if request.user.user_type != 'business':
            return Response({"error": "You are not Business User"}, status=400)
        
        #request.data['user'] = request.user.id  # Assign the current logged-in user
        mutable_data = request.data.copy()  # Create a mutable copy
        mutable_data["user"] = request.user.id  # Modify the data


        serializer = BusinessInfoSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Business Info created successfully", "data": serializer.data}, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk=None):
        """Partial update business info by ID"""
        try:
            if request.user.user_type != 'business':
                return Response({"error": "You are not Business User"}, status=400)
            
            business_info = BusinessInfo.objects.get(id=pk)
            serializer = BusinessInfoSerializer(business_info, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Business Info updated successfully", "data": serializer.data}, status=200)
            return Response(serializer.errors, status=400)
        except BusinessInfo.DoesNotExist:
            return Response({"error": "Business Info not found"}, status=404)

    # def delete(self, request, pk=None):
    #     """Delete business info by ID"""
    #     try:
    #         business_info = BusinessInfo.objects.get(id=pk, user=request.user)
    #         business_info.delete()
    #         return Response({"message": "Business Info deleted successfully"})
    #     except BusinessInfo.DoesNotExist:
    #         return Response({"error": "Business Info not found"}, status=404)



class BusinessSearchView(APIView):
    def get(self, request):
        query = request.GET.get("query", "")

        if not query:
            businesses = BusinessInfo.objects.all()
        else:
            businesses = BusinessInfo.objects.filter(
                Q(business_name__icontains=query) | Q(business_type__icontains=query)
            )

        serializer = BusinessInfoSerializer(businesses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BusinessDetailView(APIView):
    def get(self, request, business_id):
        try:
            business = BusinessInfo.objects.get(id=business_id)
        except BusinessInfo.DoesNotExist:
            return Response({"error": "Business not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BusinessInfoSerializer(business)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


########################## REQUESTS ##########################
# User business join request send karega
class BusinessJoinRequestView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        business_id = request.data.get("business_id")

        if not user_id or not business_id:
            return Response({"error": "User ID and Business ID are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Objects fetch karo
        try:
            business = BusinessInfo.objects.get(id=business_id)
        except BusinessInfo.DoesNotExist:
            return Response({"error": "Business not found"}, status=status.HTTP_404_NOT_FOUND)

        # Agar user pehle se member hai
        if BusinessMembership.objects.filter(user_id=user_id, business=business).exists():
            return Response({"message": "User is already a member"}, status=status.HTTP_400_BAD_REQUEST)

        # Pehle se request pending hai?
        if MembershipRequest.objects.filter(user_id=user_id, business=business, status="pending").exists():
            return Response({"message": "Request already pending"}, status=status.HTTP_400_BAD_REQUEST)

        # Naya request create karo
        membership_request = MembershipRequest.objects.create(user_id=user_id, business=business)
        return Response({"message": "Request sent successfully"}, status=status.HTTP_201_CREATED)



# Business Owner request accept/reject karega
class ApproveMembershipRequestView(APIView):
    def put(self, request, request_id):
        action = request.data.get("action")  # "accept" or "reject"

        # Membership request fetch karo
        try:
            membership_request = MembershipRequest.objects.get(id=request_id)
        except MembershipRequest.DoesNotExist:
            return Response({"error": "Membership request not found"}, status=status.HTTP_404_NOT_FOUND)

        if action == "accept":
            membership_request.accept()
            return Response({"message": "Request accepted successfully"}, status=status.HTTP_200_OK)

        elif action == "reject":
            membership_request.reject()
            return Response({"message": "Request rejected"}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)



# User ke current business memberships dekhne ke liye
class MyBusinessMembershipsView(APIView):
    def get(self, request, user_id):
        try:
            memberships = BusinessMembership.objects.filter(user_id=user_id)
            if not memberships.exists():
                return Response({"message": "No memberships found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = BusinessMembershipSerializer(memberships, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class AchievementListCreateAPIView(APIView):
    """List and Create Achievements by User ID"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Retrieve all achievements related to the logged-in user's business"""
        business = BusinessInfo.objects.filter(user=request.user).first()
        if not business:
            return Response({"error": "Business not found"}, status=status.HTTP_404_NOT_FOUND)

        achievements = Achievement.objects.filter(business=business)
        serializer = AchievementSerializer(achievements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new achievement for the logged-in user's business"""
        business = BusinessInfo.objects.filter(user=request.user).first()
        if not business:
            return Response({"error": "Business not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AchievementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(business=business)
            return Response(
                {"message": "Achievement created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AchievementDetailAPIView(APIView):
    """Retrieve, Update, or Delete Achievement by ID"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        """Retrieve an achievement by ID"""
        achievement = Achievement.objects.filter(id=id, business__user=request.user).first()
        if not achievement:
            return Response({"error": "Achievement not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AchievementSerializer(achievement)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        """Update an achievement by ID"""
        achievement = Achievement.objects.filter(id=id, business__user=request.user).first()
        if not achievement:
            return Response({"error": "Achievement not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AchievementSerializer(achievement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Achievement updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """Delete an achievement by ID"""
        achievement = Achievement.objects.filter(id=id, business__user=request.user).first()
        if not achievement:
            return Response({"error": "Achievement not found"}, status=status.HTTP_404_NOT_FOUND)

        achievement.delete()
        return Response(
            {"message": "Achievement deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    



################## Notification ######################

class NotificationAPIView(APIView):
    """API to get notifications for the logged-in user"""

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Mark all notifications as read"""
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({"message": "All notifications marked as read"}, status=status.HTTP_200_OK)
    
    def patch(self, request, notification_id):
        """Mark a single notification as read"""
        try:
            notification = Notification.objects.get(id=notification_id, recipient=request.user)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if notification.is_read:
            return Response({"message": "Notification already read"}, status=status.HTTP_200_OK)

        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
    



class EquipmentMasterAPIView(APIView):
    """
    API View to handle Equipment Master CRUD operations.
    """
    parser_classes = (MultiPartParser, FormParser)  
    permission_classes = [IsAuthenticated]  

    def get(self, request, equipment_id=None):
        """
        Retrieve all equipment or a specific equipment by ID.
        """
        if equipment_id:
            try:
                equipment = EquipmentMaster.objects.get(id=equipment_id)
                serializer = EquipmentMasterSerializer(equipment)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except EquipmentMaster.DoesNotExist:
                return Response({"error": "Equipment not found"}, status=status.HTTP_404_NOT_FOUND)

        equipments = EquipmentMaster.objects.all()
        serializer = EquipmentMasterSerializer(equipments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new equipment entry with `created_by` set to the logged-in user.
        """
        data = request.data.copy()  # Copy data to modify it
        data["created_by"] = request.user.id  # Assign logged-in user

        serializer = EquipmentMasterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, equipment_id):
        """
        Update an existing equipment entry.
        """
        try:
            equipment = EquipmentMaster.objects.get(id=equipment_id)
        except EquipmentMaster.DoesNotExist:
            return Response({"error": "Equipment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EquipmentMasterSerializer(equipment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, equipment_id):
        """
        Delete an equipment entry.
        """
        try:
            equipment = EquipmentMaster.objects.get(id=equipment_id)
        except EquipmentMaster.DoesNotExist:
            return Response({"error": "Equipment not found"}, status=status.HTTP_404_NOT_FOUND)

        equipment.delete()
        return Response({"message": "Equipment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)