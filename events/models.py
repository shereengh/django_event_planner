from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Event(models.Model):
	organizer = models.ForeignKey(User, on_delete=models.CASCADE,)
	title = models.CharField(max_length=100)
	datetime = models.DateTimeField() 
	seats = models.PositiveIntegerField()
	location = models.CharField(max_length=100)
	description = models.TextField()

	def __str__(self):
		return self.title
	def get_absolute_url(self):
		return reverse('event-detail', kwargs={'event_id':self.id})

class Reserve(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,)
	event = models.ForeignKey(Event, on_delete=models.CASCADE,)
	amount = models.PositiveIntegerField()

	def __str__(self):
		return "%s: %s" % (self.user.username, str(self.event))
