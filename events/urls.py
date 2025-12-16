from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact')
    path('help/', views.help, name='help'),
   
    path('add/', views.add_club, name='add_club'),
    path('clubs/<slug:slug>/', views.club_detail, name='club_detail'),
    path('clubs/', views.club_list, name='club_list'),
    path('clubs/<slug:slug>/add-member/', views.add_member, name='add_member'), 
    path("add_event/", views.add_event, name="add_event"),
    path('logout/', views.user_logout, name='logout'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
     path('clubs/<slug:slug>/edit/', views.edit_club, name='edit_club'),
    path('clubs/<slug:slug>/delete/', views.delete_club, name='delete_club'),
    path('gallery/', views.galleryImages, name='club_gallery'),
    path("clubs/<slug:slug>/gallery/upload/", views.upload_image, name="upload_image"),
    path("event/<int:event_id>/feedback/", views.submit_feedback, name="submit_feedback"),
     path('accounts/', include('allauth.urls')),
]
