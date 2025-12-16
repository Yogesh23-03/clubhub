from django import forms
from .models import Club
from .models import ClubMember
from .models import Event
from .models import GalleryImage
from .models import Feedback
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)




class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name','description', 'leader', 'contact_email', 'logo', 'banner']

class ClubMemberForm(forms.ModelForm):
    class Meta:
        model = ClubMember
        fields = ['name', 'role', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 dark:border-gray-700 rounded-lg px-4 py-2 bg-white dark:bg-card-dark text-gray-900 dark:text-white',
                'placeholder': 'Member Name'
            }),
            'role': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 dark:border-gray-700 rounded-lg px-4 py-2 bg-white dark:bg-card-dark text-gray-900 dark:text-white',
                'placeholder': 'Role (e.g., President, Designer)'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'w-full border border-gray-300 dark:border-gray-700 rounded-lg px-4 py-2 bg-white dark:bg-card-dark text-gray-900 dark:text-white'
            }),
        }




from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "date",
            "time",
            "location",
            "category",
            "organizer",
            "image",
            "department",
            "club",                # new field
            "registration_link",   # new field
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800/80 text-gray-900 dark:text-gray-100",
                "placeholder": "Enter event title..."
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800/80 text-gray-900 dark:text-gray-100",
                "placeholder": "Write a short event description..."
            }),
            "date": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800/80 text-gray-900 dark:text-gray-100"
            }),
            "time": forms.TimeInput(attrs={
                "type": "time",
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800/80 text-gray-900 dark:text-gray-100"
            }),
            "location": forms.TextInput(attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800/80 text-gray-900 dark:text-gray-100",
                "placeholder": "Enter location..."
            }),
            "category": forms.TextInput(attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800/80 text-gray-900 dark:text-gray-100",
                "placeholder": "E.g., Workshop, Seminar..."
            }),
            "organizer": forms.TextInput(attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800/80 text-gray-900 dark:text-gray-100",
                "placeholder": "Event organizer..."
            }),
            "department": forms.TextInput(attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800/80 text-gray-900 dark:text-gray-100",
                "placeholder": "Department hosting the event..."
            }),
            "club": forms.Select(attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800/80 text-gray-900 dark:text-gray-100"
            }),
            "registration_link": forms.URLInput(attrs={
                "class": "w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-800/80 text-gray-900 dark:text-gray-100",
                "placeholder": "Enter registration link (e.g. https://forms.gle/...)"
            }),
        }

class GalleryForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ["image", "caption"]


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "email", "message"]