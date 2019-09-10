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
	picture = models.ImageField(blank=True, null=True)

	def __str__(self):
		return self.title
	def get_absolute_url(self):
		return reverse('event-detail', kwargs={'event_id':self.id})

	def num_seats(self):
		total = 0
		for item in self.reserves.all():
			total += item.amount
		return total

	def left_seats(self):
		return self.seats - self.num_seats()

	def is_full(self):
		if self.left_seats()==0:
			return True 
		else:
			return False

	def track_user(self):
		for item in self.reserves.all():
			print(item.user.username)

class Reserve(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reserves')
	amount = models.PositiveIntegerField()

	def __str__(self):
		return "%s: %s" % (self.user.username, str(self.event))
