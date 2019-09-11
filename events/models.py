from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
import math
from django.dispatch import receiver
from django.db.models.signals import post_save

class Event(models.Model):
	organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
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
		return sum(self.reserves.all().values_list('amount', flat=True))

	def left_seats(self):
		return self.seats - self.num_seats()

	def is_full(self):
		return self.left_seats()==0
	
	def can_cancel(self):
		diff = (self.datetime.replace(tzinfo=None) - datetime.now())
		return (diff.days * 24 + diff.seconds // 3600)> 3

class Reserve(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reserves')
	amount = models.PositiveIntegerField()

	def __str__(self):
		return "%s: %s" % (self.user.username, str(self.event))


class Profile(models.Model):
	# switch to one to one
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	profilepic = models.ImageField(blank=True, null=True)
	bio = models.TextField()
	def __str__(self):
		return str(self.user)


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
	if kwargs.get('created', False):
		Profile.objects.get_or_create(user= kwargs.get('instance'),)