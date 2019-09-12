
from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
#from rest_framework.views import APIView
from datetime import datetime
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from events.models import Event, Reserve
from .serializers import EventSerializer, ReserveSerializer, RegisterSerializer, CreateEventSerializer#, ReserveCreateSerializer
from .permissions import IsOrganizer, IsAvailable
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
	permission_classes = [IsAuthenticated]
	
	def get_queryset(self):
		return Reserve.objects.filter(event_id=self.kwargs['event_id'])
'''
class CreateBook(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request, event_id):
		reserve = request.data.get('reserve')

		serializer = ReserveSerializer(data=reserve)
		if serializer.is_valid(raise_exception=True):
			reserve_obj = serializer.save(commit=False)
			seats =reserve_obj.amount
			capacity = reserve_obj.left_seats()
			if seats > capacity:
				return Response({"error": "Booking exceeds amount of seats left!"})
			else:
				reserve_obj = serializer.save()


		return Response()	
'''


class OrganizerEventsList(ListAPIView):
	serializer_class = CreateEventSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Event.objects.filter(organizer_id=self.kwargs['organizer_id'])