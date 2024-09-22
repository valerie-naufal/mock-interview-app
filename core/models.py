from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    mobile_number = models.CharField(max_length=50, blank=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say'),
    )
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)


class InterviewCategory(models.Model):
    name = models.CharField(max_length=50)

class Interview(models.Model):
    interviewer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    interview_date = models.DateField(null=True)
    interview_time = models.TimeField(null=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    booked = models.BooleanField(default=False)  


class Payment(models.Model):
    PAYMENT_CHOICES = (
        ('Cash', 'Cash'),
        ('Online', 'Online'),
    )
    payment = models.CharField(max_length=200, choices=PAYMENT_CHOICES)


class Booking(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.SET_NULL, blank=True, null=True)
    interviewer = models.ForeignKey(User, related_name='interviewer_bookings', on_delete=models.SET_NULL, blank=True, null=True)
    interviewee = models.ForeignKey(User, related_name='interviewee_bookings', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)


class Feedback(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    communication_skills = models.FloatField(null=True)
    professionalism = models.FloatField(null=True)
    adaptability =  models.FloatField(null=True)
    preparation = models.FloatField(null=True)
    competency = models.FloatField(null=True)
    time_management = models.FloatField(null=True)
    overall_effectiveness = models.TextField(null=True)
    
     
