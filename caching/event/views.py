from django.shortcuts import HttpResponse
from django.http import Http404
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from event.models import Event, Guest

from event.serializers import EventSerializer, GuestSerializer

CACHE_TTL = 60 * 15
USE_CACHE = True
INVALIDATE_CACHE = True
USE_IMPROVED_Query = True

def index(requests):
    return HttpResponse('<b>Welcome to Caching with Redis Course!</b>')

class EventList(APIView):
    def get(self, request):

        if USE_CACHE:
            events = cache.get('events')
            if events is not None:
                return Response(events)
            event = Event.objects.all()
            serializer = EventSerializer(event, many=True)
            cache.set('events', serializer.data, CACHE_TTL)
            return Response(serializer.data)

        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if INVALIDATE_CACHE:
                cache.delete('events')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        if USE_CACHE:
            event = cache.get('event_%s' % pk)
            if event is not None:
                return Response(event)

        event = self.get_object(pk)
        serializer = EventSerializer(event)

        if USE_CACHE:
            cache.set('event_%s' % pk, serializer.data, CACHE_TTL)

        return Response(serializer.data)

    def put(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if INVALIDATE_CACHE:
                cache.delete('event_%s' % pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = self.get_object(pk)
        event.delete()
        if INVALIDATE_CACHE:
            cache.delete('event_%s' % pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GuestList(APIView):
    def get(self, request):
        if USE_CACHE:
            guests = cache.get('guests')
            if guests is not None:
                return Response(guests)

            if USE_IMPROVED_Query:
                guests = Guest.objects.all().select_related('event')[:10]
            else:
                guests = Guest.objects.all()[:10]
            serializer = GuestSerializer(guests, many=True)
            cache.set('guests', serializer.data, CACHE_TTL)
            return Response(serializer.data)

        if USE_IMPROVED_Query:
            guests = Guest.objects.all().select_related('event')[:10]
        else:
            guests = Guest.objects.all()[:10]
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GuestDetail(APIView):
    def get_object(self, pk):
        try:
            if USE_IMPROVED_Query:
                return Guest.objects.select_related('event').get(pk=pk)
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        if USE_CACHE:
            guest = cache.get('guest_%s' % pk)
            if guest is not None:
                return Response(guest)

        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        if USE_CACHE:
            cache.set('guest_%s' % pk, serializer.data, CACHE_TTL)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if INVALIDATE_CACHE:
                cache.delete('guest_%s' % pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        if INVALIDATE_CACHE:
            cache.delete('guest_%s' % pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
