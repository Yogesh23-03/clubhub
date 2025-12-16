from django.contrib import admin
from .models import Event, Club, Profile, ClubMember


# Register your models here.
admin.site.register(Event)
admin.site.register(Club)
admin.site.register(Profile)
admin.site.register(ClubMember)
