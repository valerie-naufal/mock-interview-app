from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Avg
from .models import UserProfile
from django.contrib import messages
from .models import Interview, Booking, Feedback
from django.core.mail import send_mail
from django.conf import settings

def main(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print("login successfull")
            login(request, user)
            return redirect('home')  
        else:
            print("failed to login: ", request)
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'index.html')

def create(request):
    if request.method == 'POST':
        print("alo alo")
        # Get data from the form
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password1') 
        gender = request.POST.get('gender')
        mobile_number = request.POST.get('mobile_number')
        date_of_birth = request.POST.get('date_of_birth')
        image = request.FILES.get('image')

        # Create a new User object
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Create a new UserProfile object
        user_profile = UserProfile.objects.create(
            user=user,
            mobile_number=mobile_number,
            gender=gender,
            date_of_birth=date_of_birth,
        )

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print('User authenticated and logged in successfully!')
            return redirect('home')  
        else:
            print('Failed to authenticate user!')
            # Handle authentication failure 
            return render(request, 'login.html')

    return render(request, 'create-account.html')

def profile(request):
    user = request.user
    user_bookings = Booking.objects.filter(Q(interviewer=user) | Q(interviewee=user))

    # Extracting booking IDs from user_bookings
    booking_ids = user_bookings.values_list('id', flat=True)

    # Retrieving related feedbacks
    related_feedbacks = Feedback.objects.filter(booking__id__in=booking_ids)

    # Calculating average grades for each feedback criterion
    average_communication_skills = related_feedbacks.aggregate(Avg('communication_skills'))['communication_skills__avg']
    average_professionalism = related_feedbacks.aggregate(Avg('professionalism'))['professionalism__avg']
    average_adaptability = related_feedbacks.aggregate(Avg('adaptability'))['adaptability__avg']
    average_preparation = related_feedbacks.aggregate(Avg('preparation'))['preparation__avg']
    average_competency = related_feedbacks.aggregate(Avg('competency'))['competency__avg']
    average_time_management = related_feedbacks.aggregate(Avg('time_management'))['time_management__avg']

    return render(request, 'my-profile.html', {
        'user': user,
        'user_bookings': user_bookings,
        'related_feedbacks': related_feedbacks,
        'average_communication_skills': average_communication_skills,
        'average_professionalism': average_professionalism,
        'average_adaptability': average_adaptability,
        'average_preparation': average_preparation,
        'average_competency': average_competency,
        'average_time_management': average_time_management,
    })


def bookings(request):
    return render(request, 'bookings.html')

def statistics(request):
    return render(request, 'statistics.html')

def host(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        category = request.POST.get('category')
        price = request.POST.get('price')

        # Create a new Interview object with the submitted data
        interview = Interview.objects.create(
            interviewer=request.user,
            interview_date=date,
            interview_time=time,
            category=category,
            price=price
        )
        print('Interview created successfully!')
        return render(request, 'created.html')
    print("No interview getting created")
    return render(request,'host.html')

def book(request):
    if request.method == 'POST':
        interview_id = request.POST.get('interview_id')
        # Retrieve the interview object
        interview = Interview.objects.get(pk=interview_id)
        
        # Check if the interview is not already booked
        if not interview.booked:
            # Set the interview as booked
            interview.booked = True
            interview.save()
        # Create the Booking object
        booking = Booking.objects.create(
            interview=interview,
            interviewer=interview.interviewer,
            interviewee=request.user,
        )
        print('Booking created successfully!')
    return render(request, 'booked.html')



def feedback(request):
    bookings = Booking.objects.all().order_by('-id')


    context = {
        'bookings': bookings,
    }
    return render(request,'feedback.html', context)

def home(request):
    interviews = Interview.objects.all()
    return render(request, 'home.html', {'interviews': interviews})

#view function for submitting the host interview inputs 
def host_interview_form(request):
    if request.method == 'POST':
        category = request.POST.get("category")
        date = request.POST.get("date")
        time = request.POST.get("time")
        price = request.POST.get("price")
        print(category, " ",date," ",time," ",price)
    return render(request,'home.html')

def feedback_form(request):
    if request.method == 'POST':
        booking_id = request.POST.get("booking_id")
        booking = get_object_or_404(Booking, id=booking_id)
        communication_skills = request.POST.get("communication_skills")
        professionalism = request.POST.get("professionalism")
        adaptability = request.POST.get("adaptability")
        preparation = request.POST.get("preparation")
        competency = request.POST.get("competency")
        time_management = request.POST.get("time_management")
        overall_effectiveness = request.POST.get("overall_effectiveness")

        feedback = Feedback.objects.create(
            booking = booking,
            communication_skills = communication_skills,
            professionalism = professionalism,
            adaptability = adaptability,
            preparation = preparation,
            competency = competency,
            time_management = time_management,
            overall_effectiveness = overall_effectiveness
        )

        interviewee_email = booking.interviewee.email

        subject = f"Feedback for interview {booking.interview.id} is ready"
        message = f"Hello {booking.interviewee.username}!\n\n"
        message += f"Your feedback for interview {booking.interview.id} is ready. "
        message += "Find below the provided info by your interviewer:\n"
        message += f"Communication skills: {communication_skills}/5\n"
        message += f"Professionalism: {professionalism}/5\n"
        message += f"Adaptability: {adaptability}/5\n"
        message += f"Preparation: {preparation}/5\n"
        message += f"Competency: {competency}/5\n"
        message += f"Time management: {time_management}/5\n"
        message += f"Overall Effectiveness: {overall_effectiveness}\n\n"
        message += "If you are happy about your results, congrats! Otherwise, you can still book other interviews on the platform.\n\n"
        message += "Note that interview_me is not responsible for the content provided in this feedback.\n\n"
        message += "Good luck!"

        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [interviewee_email])

    return render(request,'feedback_submitted.html')


def logout(request):
    logout(request)
    return(request, 'home.html')
