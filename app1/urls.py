from django.urls import path
from .views import *

urlpatterns = [

    path('register-user', RegisterAPIView.as_view()),
    path("all-doctors",AllDoctors.as_view()),
    path('doctors',DoctorListView.as_view()),
    path("logout", LogoutView.as_view()),
    path("doctor/<int:pk>",GetCreateDoctorAPI.as_view()),
    path("book-appointment",BookAppointment.as_view()),
    path('my-profile',MyprofileView.as_view()),

]
