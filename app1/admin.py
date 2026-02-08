from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomeUser)
admin.site.register(Department)
admin.site.register(ProfileDetails)
admin.site.register(SheduleDetails)
admin.site.register(AppointmentDetails)

