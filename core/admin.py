from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(InterviewCategory)
admin.site.register(Interview)
admin.site.register(Payment)
admin.site.register(Booking)
admin.site.register(Feedback)