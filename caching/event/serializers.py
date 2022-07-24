from rest_framework.serializers import ModelSerializer

from event.models import Event, Guest

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'location', 'description')
        read_only_fields = ('id',)

class GuestSerializer(ModelSerializer):
    event = EventSerializer(read_only=True)
    class Meta:
        model = Guest
        fields = ('id', 'event', 'name', 'email')
        read_only_fields = ('id',)
        extra_kwargs = {
            'event': {'required': True},
        }
