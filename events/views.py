
from django.shortcuts import get_object_or_404, render,redirect
from .models import Event,Club
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from events.forms import ClubMemberForm, ContactForm,ClubForm
from .forms import EventForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from .forms import GalleryForm, FeedbackForm
from .models import GalleryImage
from .models import Feedback
from django.utils import timezone
# Create your views here.

def home(request):
    upcoming_events = Event.objects.filter(
        date__gte=timezone.now().date()
    ).order_by('date')[:4]

    compliments = Feedback.objects.order_by('-submitted_at')[:3]

    context = {
        'upcoming_events': upcoming_events,
        'compliments': compliments,
    }
    return render(request, 'home.html', context)

def events(request):
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    Event.objects.filter(date__lt=thirty_days_ago).delete()
    events =Event.objects.all()
    context={
        'events':events
    }
    return render(request, 'events.html',context)

@login_required(login_url='login')
@permission_required('events.add_event', raise_exception=True)
def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})



def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events_detail.html', {'event': event})



def about(request):
    return render(request, 'about.html')

def help(request):
    faqs = [
        {"question": "How do I register for an event?", "answer": "Go to the Events page, click on your preferred event, and follow the registration link."},
        {"question": "Can I edit my registration details later?", "answer": "Yes, you can modify your registration details before the event starts."},
        {"question": "How do I contact the event organizers?", "answer": "You can find organizer details on each event’s detail page."},
        {"question": "Is there a participation fee?", "answer": "Some events may have fees depending on the organizing department."},
    ]
    return render(request, 'help.html', {"faqs": faqs})



def assign_permissions(user, role):
    """Assign permissions based on user role."""
    event_ct = ContentType.objects.get_for_model(Event)
    club_ct = ContentType.objects.get_for_model(Club)

    if role == 'organizer':
        # Full CRUD access to Event model
        event_perms = Permission.objects.filter(
            content_type=event_ct,
            codename__in=['add_event', 'change_event', 'delete_event', 'view_event']
        )
        club_perms=Permission.objects.filter(
            content_type=club_ct,
            codename__in=['add_club', 'change_club', 'delete_club', 'view_club','add_member']
        )
        user.user_permissions.set(list(event_perms) + list(club_perms))

    elif role == 'faculty':
        # Can view and edit, but not delete or add
        event_perms = Permission.objects.filter(
            content_type=event_ct,
            codename__in=['change_event', 'view_event']
        )
        club_perms = Permission.objects.filter(
            content_type=club_ct,
            codename__in=['change_club', 'view_club']
        )
        user.user_permissions.set(list(event_perms) + list(club_perms))

    elif role == 'student':
        # Only view events
        event_perms = Permission.objects.filter(
            content_type=event_ct,
            codename__in=['view_event']
        )
        club_perms = Permission.objects.filter(
            content_type=club_ct,
            codename__in=['view_club']
        )
        user.user_permissions.set(list(event_perms) + list(club_perms))

    user.save()






def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        # Password validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        # Check if email already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password1, 
            first_name=full_name
        )

        # Create Profile and assign role
        Profile.objects.create(user=user, role=role)

        # Assign permissions based on role
        assign_permissions(user, role)

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'register.html')


@login_required(login_url='login')
@permission_required('events.change_club', raise_exception=True)
def edit_club(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, 'Club updated successfully!')
            return redirect('club_detail', slug=club.slug)
        else:
            messages.error(request, f"Error: {form.errors.as_text()}")
    else:
        form = ClubForm(instance=club)
    return render(request, 'create_club.html', {'form': form, 'club': club})


@login_required(login_url='login')
@permission_required('events.delete_club', raise_exception=True)
def delete_club(request, slug):
    """Delete a club"""
    club = get_object_or_404(Club, slug=slug)
    if request.method == 'POST':
        club.delete()
        messages.success(request, 'Club deleted successfully!')
        return redirect('club_list')
    return render(request, 'confirm_delete_club.html', {'club': club})





def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # redirect after login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')



@login_required(login_url='login')
@permission_required('events.add_club', raise_exception=True)
def add_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)
            club.slug = slugify(club.name)
            club.save()
            messages.success(request, "✅ Club added successfully!")
            return redirect('club_list')
        else:
            print("Form errors:", form.errors)  # Debugging
            messages.error(request, "Please correct the errors below.")
    else:
        form = ClubForm()
    return render(request, 'create_club.html', {'form': form})



from django.utils import timezone

def club_detail(request, slug):
    club = get_object_or_404(Club, slug=slug)

    # Filtering logic
    filter_type = request.GET.get("filter", "upcoming")

    today = timezone.now().date()

    if filter_type == "past":
        events = club.events.filter(date__lt=today).order_by('-date')
    else:  # upcoming
        events = club.events.filter(date__gte=today).order_by('date')

    context = {
        "club": club,
        "events": events,
        "filter_type": filter_type,
    }

    return render(request, "club_detail.html", context)





def club_list(request):
    query = request.GET.get('q', '')  # get search term from ?q=
    clubs = Club.objects.all()

    if query:
        clubs = clubs.filter(name__icontains=query) | clubs.filter(description__icontains=query) | clubs.filter(leader__icontains=query)

    return render(request, 'all_clubs.html', {'clubs': clubs, 'query': query})


@login_required(login_url='login')
@permission_required('events.add_member', raise_exception=True)
def add_member(request, slug):
    club = get_object_or_404(Club, slug=slug)

    if request.method == 'POST':
        form = ClubMemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.club = club
            member.save()
            return redirect('club_detail', slug=club.slug)
    else:
        form = ClubMemberForm()

    return render(request, 'add_member.html', {'form': form, 'club': club})


@login_required(login_url='login')
@permission_required('events.change_event', raise_exception=True)
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = EventForm(instance=event)
    return render(request, 'add_event.html', {'form': form, 'event': event})

@login_required(login_url='login')
@permission_required('events.delete_event', raise_exception=True)
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('events')

login_required
@permission_required('events.change_club', raise_exception=True)
def upload_image(request, slug):
    club = get_object_or_404(Club, slug=slug)

    if request.method == "POST":
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.club = club
            gallery.save()
            return redirect("club_gallery")
    else:
        form = GalleryForm()

    return render(request, "upload_images.html", {"form": form, "club": club})
def galleryImages(request):
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, "gallary.html", {"images": images})

def submit_feedback(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.event = event
            feedback.save()

            messages.success(request, "Thank you for your feedback!")
            return redirect('event_detail', event_id=event.id)

    else:
        form = FeedbackForm()

    return render(request, "feedbackform.html", {"form": form, "event": event})
