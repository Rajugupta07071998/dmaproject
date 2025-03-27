from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import WeeklyPlan, SubTask, Batch, MasterPolicy, Attendance
from .serializers import (
    WeeklyPlanSerializer, SubTaskSerializer, BatchSerializer,
    MasterPolicySerializer, AttendanceSerializer
)
from account.models import User
from core.models import BusinessMembership
from datetime import datetime



# Helper Function to Filter Business User Data
def get_user_queryset(queryset, user):
    """Returns only the objects created by the authenticated business user."""
    return queryset.filter(created_by=user)


# Weekly Plan API
class WeeklyPlanAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = get_user_queryset(WeeklyPlan.objects.all(), request.user)
        serializer = WeeklyPlanSerializer(plans, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = WeeklyPlanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# SubTask API
class SubTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = get_user_queryset(SubTask.objects.all(), request.user)
        serializer = SubTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = SubTaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Batch API
class BatchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        batches = get_user_queryset(Batch.objects.all(), request.user)
        serializer = BatchSerializer(batches, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = BatchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# MasterPolicy API
class MasterPolicyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        policies = get_user_queryset(MasterPolicy.objects.all(), request.user)
        serializer = MasterPolicySerializer(policies, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = MasterPolicySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Attendance API
# class AttendanceAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         attendance_records = get_user_queryset(Attendance.objects.all(), request.user)
#         serializer = AttendanceSerializer(attendance_records, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         data = request.data.copy()
#         data['created_by'] = request.user.id
#         serializer = AttendanceSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







### -------------------- Weekly Plan APIs -------------------- ###
class WeeklyPlanDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            plan = WeeklyPlan.objects.get(id=pk, created_by=request.user)
            serializer = WeeklyPlanSerializer(plan)
            return Response(serializer.data)
        except WeeklyPlan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            plan = WeeklyPlan.objects.get(id=pk, created_by=request.user)
            serializer = WeeklyPlanSerializer(plan, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except WeeklyPlan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            plan = WeeklyPlan.objects.get(id=pk, created_by=request.user)
            plan.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except WeeklyPlan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)


### -------------------- SubTask APIs -------------------- ###
class SubTaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            task = SubTask.objects.get(id=pk, created_by=request.user)
            serializer = SubTaskSerializer(task)
            return Response(serializer.data)
        except SubTask.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            task = SubTask.objects.get(id=pk, created_by=request.user)
            serializer = SubTaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SubTask.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            task = SubTask.objects.get(id=pk, created_by=request.user)
            task.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except SubTask.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)


### -------------------- Batch APIs -------------------- ###
class BatchDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            batch = Batch.objects.get(id=pk, created_by=request.user)
            serializer = BatchSerializer(batch)
            return Response(serializer.data)
        except Batch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            batch = Batch.objects.get(id=pk, created_by=request.user)
            serializer = BatchSerializer(batch, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Batch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            batch = Batch.objects.get(id=pk, created_by=request.user)
            batch.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Batch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND)


### -------------------- Master Policy APIs -------------------- ###
class MasterPolicyDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            policy = MasterPolicy.objects.get(id=pk, created_by=request.user)
            serializer = MasterPolicySerializer(policy)
            return Response(serializer.data)
        except MasterPolicy.DoesNotExist:
            return Response({"error": "Policy not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            policy = MasterPolicy.objects.get(id=pk, created_by=request.user)
            serializer = MasterPolicySerializer(policy, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MasterPolicy.DoesNotExist:
            return Response({"error": "Policy not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            policy = MasterPolicy.objects.get(id=pk, created_by=request.user)
            policy.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except MasterPolicy.DoesNotExist:
            return Response({"error": "Policy not found"}, status=status.HTTP_404_NOT_FOUND)


### -------------------- Attendance APIs -------------------- ###
# class AttendanceDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk):
#         try:
#             record = Attendance.objects.get(id=pk, created_by=request.user)
#             serializer = AttendanceSerializer(record)
#             return Response(serializer.data)
#         except Attendance.DoesNotExist:
#             return Response({"error": "Attendance record not found"}, status=status.HTTP_404_NOT_FOUND)

#     def patch(self, request, pk):
#         try:
#             record = Attendance.objects.get(id=pk, created_by=request.user)
#             serializer = AttendanceSerializer(record, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Attendance.DoesNotExist:
#             return Response({"error": "Attendance record not found"}, status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, pk):
#         try:
#             record = Attendance.objects.get(id=pk, created_by=request.user)
#             record.delete()
#             return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
#         except Attendance.DoesNotExist:
#             return Response({"error": "Attendance record not found"}, status=status.HTTP_404_NOT_FOUND)




class BatchAttendanceAPIView(APIView):
    """
    API for batch-wise attendance marking.
    
    - `GET`: List all users in the batch for selection.
    - `POST`: Mark attendance for selected users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, batch_id):
        """
        Retrieve all users in a given batch.
        Only the batch creator (business user) can view the users.

        GET /batch/{batch_id}/attendance/
        Returns a list of all users in the batch.
        The frontend will display a list with checkboxes for selection.
        """
        try:
            batch = Batch.objects.get(id=batch_id, created_by=request.user)  # Ensure only creator can access

            # Assuming users are linked to the batch via the WeeklyPlan
            users_in_batch = User.objects.filter(batches=batch)

            user_list = [{"id": user.id, "name": user.get_full_name()} for user in users_in_batch]

            return Response({"batch_id": batch.id, "batch_name": batch.name, "users": user_list}, status=status.HTTP_200_OK)

        except Batch.DoesNotExist:
            return Response({"error": "Batch not found or unauthorized access"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, batch_id):
        """
        Mark attendance for selected users in a batch.
        - Ensures users belong to the batch before marking attendance.
        - Prevents duplicate attendance entries.
        - Allows bulk attendance marking.

        POST /batch/{batch_id}/attendance/
        Marks attendance for selected users.
        Prevents duplicate entries.
        """
        try:
            batch = Batch.objects.get(id=batch_id, created_by=request.user)  # Only batch creator can mark attendance
            data = request.data

            user_ids = data.get("user_ids", [])
            date = data.get("date")
            status_value = data.get("status", "present")  # Default status = "present"

            if not user_ids or not date:
                return Response({"error": "user_ids and date are required"}, status=status.HTTP_400_BAD_REQUEST)

            attendance_entries = []
            already_marked = []

            for user_id in user_ids:
                try:
                    user = User.objects.get(id=user_id)

                    # Ensure user belongs to this batch
                    if not batch.weekly_plan or user not in batch.weekly_plan.batches.all():
                        return Response({"error": f"User {user_id} is not part of Batch {batch_id}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    # Check for duplicate attendance
                    if Attendance.objects.filter(batch=batch, user=user, date=date).exists():
                        already_marked.append(user_id)
                        continue  # Skip already marked users
                    
                    attendance_entry = Attendance(
                        batch=batch,
                        user=user,
                        date=date,
                        status=status_value,
                        created_by=request.user
                    )
                    attendance_entries.append(attendance_entry)
                except User.DoesNotExist:
                    return Response({"error": f"User {user_id} not found"}, status=status.HTTP_400_BAD_REQUEST)

            # Bulk create new attendance records
            Attendance.objects.bulk_create(attendance_entries)

            response_data = {"message": "Attendance marked successfully"}
            if already_marked:
                response_data["skipped_users"] = already_marked  # Users whose attendance was already marked
            
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Batch.DoesNotExist:
            return Response({"error": "Batch not found or unauthorized access"}, status=status.HTTP_404_NOT_FOUND)





class AssignBatchAPIView(APIView):
    """
    API to assign a batch to a user if they belong to a BusinessMembership.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_id):
        """Retrieve all business members eligible for batch assignment."""
        members = User.objects.filter(business_memberships__business_id=business_id)
        data = [{"id": str(member.id), "name": member.get_full_name()} for member in members]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, user_id, batch_id):
        """
        Assign a batch to a user if they belong to a BusinessMembership.
        URL: /api/assign-batch/{user_id}/{batch_id}/
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            batch = Batch.objects.get(id=batch_id)
        except Batch.DoesNotExist:
            return Response(
                {"error": "Batch not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate if user belongs to a business membership
        # if not BusinessMembership.objects.filter(user=user).exists():
        #     return Response(
        #         {"error": "User is not part of any business membership."},
        #         status=status.HTTP_403_FORBIDDEN,
        #     )

        # Assign batch to the user
        user.batch_policy = batch
        user.save()

        return Response(
            {"message": f"Batch '{batch.name}' assigned to {user.get_full_name()}"},
            status=status.HTTP_200_OK,
        )
    


class BatchWiseMembersAPIView(APIView):
    """
    API to list all members assigned to a specific batch.

    Endpoints:
        - GET `/api/batch-members/{batch_id}/`
            -> Retrieves all users assigned to the given batch.

    Permissions:
        - Only authenticated users can access this API.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, batch_id):
        """
        Retrieve a list of users assigned to a specific batch.

        Args:
            - batch_id (int): The ID of the batch.

        Returns:
            - 200 OK: List of users assigned to the batch.
            - 404 Not Found: If no users are found for the batch.
        """
        try:
            batch = Batch.objects.get(id=batch_id)
        except Batch.DoesNotExist:
            return Response(
                {"error": "Batch not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Fetch users assigned to this batch
        members = User.objects.filter(batch_policy=batch)

        if not members.exists():
            return Response(
                {"error": "No members found for this batch."},
                status=status.HTTP_404_NOT_FOUND
            )

        data = [
            {"id": str(member.id), "name": member.get_full_name(), "user_type": member.user_type}
            for member in members
        ]

        return Response(data, status=status.HTTP_200_OK)
    





class AttendanceReportAPIView(APIView):
    """
    API to retrieve attendance reports with multiple filters.

    - `GET /attendance-report/`
        Retrieves all attendance records.
    - Supports filtering by:
        - `user_id`: Get attendance for a specific user.
        - `batch_id`: Get attendance for a specific batch.
        - `start_date` & `end_date`: Filter attendance within a date range.
        - `status`: Get attendance for a specific status (Present, Absent, etc.).
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Retrieve attendance records with optional filters.

        Query Parameters:
        - `user_id` (optional): Filter attendance for a specific user.
        - `batch_id` (optional): Filter attendance for a specific batch.
        - `start_date` (optional): Start date for filtering (YYYY-MM-DD).
        - `end_date` (optional): End date for filtering (YYYY-MM-DD).
        - `status` (optional): Filter by attendance status (present, absent, leave, holiday).

        Returns:
        - 200 OK: List of filtered attendance records.
        - 400 Bad Request: If date format is incorrect.
        """
        user_id = request.GET.get("user_id")
        batch_id = request.GET.get("batch_id")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        status_filter = request.GET.get("status")

        # Base queryset
        attendance_records = Attendance.objects.filter(created_by=request.user).order_by('-created_at')

        # Apply filters if provided
        if user_id:
            attendance_records = attendance_records.filter(user_id=user_id)
        if batch_id:
            attendance_records = attendance_records.filter(batch_id=batch_id)
        if status_filter:
            attendance_records = attendance_records.filter(status=status_filter)
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                attendance_records = attendance_records.filter(date__range=[start_date, end_date])
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize attendance records
        report_data = [
            {
                "user_id": str(record.user.id),
                "user_name": record.user.get_full_name(),
                "batch_id": record.batch.id if record.batch else None,
                "batch_name": record.batch.name if record.batch else "N/A",
                "date": record.date.strftime("%Y-%m-%d"),
                "status": record.status,
            }
            for record in attendance_records
        ]

        return Response({"attendance_records": report_data}, status=status.HTTP_200_OK)