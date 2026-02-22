
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
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


class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]

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



class AllDoctors(APIView):

    def get(self, request):
        user = request.user
        queryset = CustomeUser.objects.filter()

        serializer = UserDetailsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class DoctorListView(APIView):

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

class GetCreateDoctorAPI(APIView):

    permission_classes = [AllowAny]  # since you want public

    def get(self, request, pk):
        profile = get_object_or_404(
            ProfileDetails.objects.select_related("user", "department"),
            user__id=pk,
            user__role="doctor"
        )

        data = {
            "doctor_id": profile.user.id,
            "username": profile.user.username,
            "first_name": profile.user.first_name,
            "last_name": profile.user.last_name,
            "full_name": f"{profile.user.first_name} {profile.user.last_name}",
            "email": profile.user.email,
            "mobile_no": profile.user.mobile_no,
            "department": profile.department.department_name if profile.department else None,
            "qualification": profile.qualification,
            "experience": profile.experience,
            "fee": profile.fee,
        }

        return Response({
            "message": "Doctor fetched successfully",
            "data": data
        }, status=status.HTTP_200_OK)


class BookAppointment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()

        # ✅ always take logged-in user as customer
        data["customer"] = request.user.id

        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
    def get(self,request):
        print("sanvededeee",request.user.id)
        data = AppointmentDetails.objects.filter(customer = request.user.id)
        print(data,"tthus us datqwert[]\][poiuytresdfghjkl;']")
        serializer = AppointmentSerializer(data,many=True)
            
        print(serializer.data,"sadhjshdjahdajk")
        return Response(serializer.data,status=201)
    
class MyprofileView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ important

    def get(self, request):
        user = request.user  # ✅ logged-in user

        serializer = MyProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)