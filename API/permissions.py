from rest_framework.permissions import BasePermission
from datetime import date


class IsOrganizer(BasePermission):
	message = "You must be the organizer of the event"

	def has_object_permission(self, request, view, obj):
		print("organizer")
		if obj.organizer == request.user:
			return True
		return False

class IsAvailable(BasePermission):
	
	message = "Booking exceeds amount of seats left!"

	def has_object_permission(self, request, view, obj):
		seats = obj.event.left_seats()
		print("Permissions")
		print(seats)
		print(obj.amount)
		if obj.amount > seats:
			return False
		return True
		