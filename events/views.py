from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm, ReserveForm, ProfileForm
from django.contrib import messages
from .models import Event, Reserve, Profile
from datetime import datetime
from django.db.models import Q
from django.core.mail import send_mail
def home(request):
    return render(request, 'home.html')

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")

def event_list(request):
    today = datetime.today()
    events = Event.objects.filter(datetime__gte=today)
    query = request.GET.get('q')
    if query:
        events = events.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(organizer__username__icontains=query)
            ).distinct()

    context = {
        "events": events ,
    }
    return render(request, 'list.html', context)

def my_event_list(request):
    # maybe use related name
    events = Event.objects.filter(organizer=request.user)
    if not events:
        messages.warning(request, "User has not organized any events")

    context = {
        "events": events,
    }
    return render(request, 'dashboard.html', context)

def event_detail(request,event_id):
    event = Event.objects.get(id=event_id)
    # maybe use related name
    reserves = Reserve.objects.filter(event=event)
    context={
    "event": event ,
    "reserves": reserves,
    }
    return render(request, "detail.html", context)


def event_create(request):
    if request.user.is_anonymous:
        return redirect('login')
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event=form.save(commit=False)
            event.organizer = request.user
            event = form.save()
            return redirect('dashboard')
    context = {
        "form":form,
    }
    return render(request, 'create.html', context)

def event_update(request, event_id):
    # Permissions
    if request.user.is_anonymous:
        return redirect('login')
    event_obj = Event.objects.get(id=event_id)
    form = EventForm(instance=event_obj)
    if request.user== event_obj.organizer:
        if request.method == "POST":
            form = EventForm(request.POST, request.FILES,instance=event_obj)
            if form.is_valid():
                form.save()
                messages.success(request, "Event has been updated successfully!")
                return redirect(event_obj)
    messages.warning(request, "You are not the organizer of the event!")
    return redirect('event-list')
    context = {
        "form":form,
        "event": event_obj,
        
    }
    return render(request, 'update.html', context)

def event_book(request,event_id):
    event= Event.objects.get(id=event_id)
    form = ReserveForm()     
    if request.method == "POST":
        form = ReserveForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.event= event
            book.user = request.user
            seats = event.left_seats()
            if book.amount > seats:
                messages.warning(request, "Booking exceeds amount of seats left!")
            else:
                book.save()
                return redirect('event-list')
                '''
            else:
                book.save()
                send_mail(
               'Your Booking Detail',
               ('This is an automated email to confirm your booking. Your booking details are: Event- {} tickets- {}'.format(book.event.title,book.amount)) ,
               'eventplanner481@gmail.com',
               ['to@example.com'],
               fail_silently=False,
               )
                return redirect("event-detail", event_id)'''
    context = {
        "form":form,
        "event":event,

    }
    return render(request, 'book.html', context)

def prev_event(request):
    today = datetime.today()
    reserves = Reserve.objects.filter(user=request.user, event__datetime__lte=today)
    context = {
        "reserves": reserves,
    }
    return render(request, 'prev.html', context)


def bookingslist(request):
    reserves = Reserve.objects.filter(user=request.user)
    context = {
        "reserves": reserves,
    }
    return render(request, 'mybookings.html', context)

def cancel_booking(request, reserve_id):
    # check 3 hour thing
    book_obj = Reserve.objects.get(id=reserve_id)
    book_obj.delete()
    messages.warning(request, "You canceled your booking!")
    return redirect('my-bookings')
'''
def create_profile(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        "profile": profile
    }
    return render(request, 'profile.html',context)
'''
def view_profile(request, user_id):
    profile = Profile.objects.get(user=user_id)
    events = Event.objects.filter(organizer=request.user)
    if not events:
        messages.warning(request, "User has not organized any events")
    context = {
        "profile": profile,
        "events": events,
    }
    return render(request, 'profile.html',context)


def profile_update(request):
    form = ProfileForm(instance=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated successfully!")
            return redirect('event-list')
    context = {
        "form":form,
    }
    return render(request, 'updateprofile.html', context)
