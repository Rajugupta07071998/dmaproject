from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PersonalInfo, BusinessInfo, Achievement
from .serializers import *


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