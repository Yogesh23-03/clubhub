from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_image_extension(value):
    valid_extensions = ['jpg', 'jpeg', 'png']
    if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError('Only JPG, JPEG, or PNG files are allowed.')

class Club(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  # for URL like /clubs/robotics/
    description = models.TextField()
    logo = models.ImageField(upload_to='club_logos/')  # jpg/png logo
    banner = models.ImageField(upload_to='club_banners/', null=True, blank=True)
    leader = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    instapage = models.URLField(blank=True)    

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    organizer = models.CharField(max_length=100)
    image= models.ImageField(upload_to='event_images/', blank=True, null=True)
    department = models.CharField(max_length=200, default="Department of CS")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    registration_link = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.title
      
    class Meta:
        ordering = ['date']

    

class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('organizer', 'Organizer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    


    
class ClubMember(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='club_members/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.role} ({self.club.name})"



class GalleryImage(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.club.name} - Image"
    
class Feedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="feedbacks")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.event.title}"
