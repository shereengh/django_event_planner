from rest_framework.permissions import BasePermission
from datetime import date


class IsOrganizer(BasePermission):
	message = "You must be the organizer of the event"

	def has_object_permission(self, request, view, obj):
		if obj.organizer == request.user:
			return True
		return False
