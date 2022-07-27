from unicodedata import name
from django.urls import path

from event import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.EventList.as_view(), name='event_list'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='event_detail'),
    path('guests/', views.GuestList.as_view(), name='guest_list'),
    path('guests/<int:pk>/', views.GuestDetail.as_view(), name='guest_detail'),
]
