from unicodedata import name
from django.urls import path

from event import views

urlpatterns = [
    path('event/', views.EventList.as_view(), name='event_list'),
    path('event/<int:pk>/', views.EventDetail.as_view(), name='event_detail'),
    path('guests/', views.GuestList.as_view(), name='guest_list'),
    path('guests/<int:pk>/', views.GuestDetail.as_view(), name='guest_detail'),
]