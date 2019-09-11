
from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from datetime import datetime
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from events.models import Event, Reserve
from .serializers import EventSerializer, ReserveSerializer, RegisterSerializer, CreateEventSerializer, ReserveCreateSerializer
from .permissions import IsOrganizer
# Create your views here.

class UpcomingEventList(ListAPIView):
	serializer_class = EventSerializer

	def get_queryset(self):
		return Event.objects.filter(datetime__gte=datetime.today())


class UserEventsList(ListAPIView):
	serializer_class = ReserveSerializer
	permission_classes = [IsAuthenticated]
	def get_queryset(self):
		return Reserve.objects.filter(user=self.request.user)


class Register(CreateAPIView):
	serializer_class = RegisterSerializer


class CreateEvent(CreateAPIView):
	serializer_class = CreateEventSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(organizer=self.request.user)



class UpdateEvent(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	serializer_class = CreateEventSerializer
	permission_classes = [IsAuthenticated, IsOrganizer]


class OrganizerEventUserList(ListAPIView):
	serializer_class = ReserveSerializer
	permission_classes = [IsAuthenticated, IsOrganizer]
	
	def get_queryset(self):
		return Reserve.objects.filter(event_id=self.kwargs['event_id'])

class CreateBook(CreateAPIView):
	serializer_class = ReserveCreateSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		event_id = self.kwargs['event_id']
		print(event_id)
		serializer.save(event_id = event_id, user = self.request.user)



class OrganizerEventsList(ListAPIView):
	serializer_class = CreateEventSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Event.objects.filter(organizer_id=self.kwargs['organizer_id'])