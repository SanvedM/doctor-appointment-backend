# from django.shortcuts import render
# from rest_framework import generics
# from .models import *
# from .serializers import *
# from rest_framework.permissions import IsAuthenticated


# # Create your views here.
# class RegisterAPIView(generics.CreateAPIView):
#     serializer_class = RegisterSerializers

# class UserDetailsAPIView(generics.ListAPIView):
#     queryset = CustomeUser.objects.filter()
#     serializer_class =UserDetailsSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
        
#         if user.is_superuser:
#             return CustomeUser.objects.all()

#         # Staff admin: see staff + normal users (exclude superusers)
#         elif user.is_staff:
#             return CustomeUser.objects.filter(is_superuser=False)
#         else:
#             return CustomeUser.objects.none()
            
# class ProfileView(generics.RetrieveUpdateAPIView):
#     serializer_class = ProfileSerializer
#     queryset = ProfileDetails
#     permission_classes = [IsAuthenticated]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetailsAPIView(APIView):

    def get(self, request):
        user = request.user
        queryset = CustomeUser.objects.filter(role="doctor")

        serializer = UserDetailsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return ProfileDetails.objects.get(pk=pk, user=user)
        except ProfileDetails.DoesNotExist:
            return None

    def get(self, request, pk):
        profile = self.get_object(pk, request.user)
        if not profile:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request, pk):
        if ProfileDetails.objects.filter(user=request.user).exists():
            return Response(
                {"error": "Profile already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProfileSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        profile = self.get_object(pk, request.user)
        if not profile:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        profile = self.get_object(pk, request.user)
        if not profile:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorProfileListView(APIView):

    def get(self, request):
        profiles = ProfileDetails.objects.select_related("user", "department").filter(
            user__role="doctor"
        )

        data = []

        for p in profiles:
            data.append({
                "doctor_id": p.user.id,  # this is used while booking appointment
                "username": p.user.username,
                "first_name": p.user.first_name,
                "last_name": p.user.last_name,
                "full_name": f"{p.user.first_name} {p.user.last_name}",
                "email": p.user.email,
                "mobile_no": p.user.mobile_no,

                "department": p.department.department_name if p.department else None,

                "qualification": p.qualification,
                "experience": p.experience,
                "fee": p.fee,
            })

        return Response({
            "message": "Doctor list fetched successfully",
            "data": data
        })


    
    
class AppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        appointment = AppointmentDetails.objects.select_related("customer")
        serializer = AppointmentSerializer(appointment, many=True)

        return Response({
            "message": "Appointment list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response({
                "message": "Appointment created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MyAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "staff":
            appointments = AppointmentDetails.objects.filter()
        else:
            appointments = AppointmentDetails.objects.filter(customer=request.user)

        serializer = AppointmentSerializer(appointments, many=True)

        return Response({
            "message": "Current user appointments fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)




class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout successful"},
                status=status.HTTP_205_RESET_CONTENT
            )

        except Exception as e:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )

