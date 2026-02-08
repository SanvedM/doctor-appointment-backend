from django.urls import path
from .views import *

urlpatterns = [

    path('register-user', RegisterAPIView.as_view()),
    path("all-doctors",DoctorDetailsAPIView.as_view()),
    path("profile/<int:pk>", ProfileView.as_view()),
    path('profiles',DoctorProfileListView.as_view()),
    path("appointment",AppointmentView.as_view()),
    path("myappointment",MyAppointmentsView.as_view()),
    path("logout", LogoutView.as_view()),


]
