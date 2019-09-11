from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
import math
from django.dispatch import receiver
from django.db.models.signals import post_save

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
	
	def can_cancel(self):
		#now=datetime.now()
		#time= now.hours+timedelta(hours=3)
		check = datetime.now()
		if (self.datetime.year <= check.year):
			if (self.datetime.month <= check.month ):
				if(self.datetime.day <= check.day):
					if((self.datetime.hour - check.hour)<3):
						return False
		return True

	def track_user(self):
		for item in self.reserves.all():
			print(item.user.username)

	def whenpublished(self):
		now = timezone.now()
		diff= now - self.datetime

		if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
			seconds= diff.seconds
			if seconds == 1:
				return str(seconds) +  "second ago"
			else:
			 return str(seconds) + " seconds ago"
		if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
			minutes= math.floor(diff.seconds/60)
			if minutes == 1:
				return str(minutes) + " minute ago"
			else:
				return str(minutes) + " minutes ago"
		if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
			hours= math.floor(diff.seconds/3600)
			if hours == 1:
				return str(hours) + " hour ago"
			else:
				return str(hours) + " hours ago"
		if diff.days >= 1 and diff.days < 30:
			days= diff.days
			if days == 1:
				return str(days) + " day ago"
			else:
				return str(days) + " days ago"
		if diff.days >= 30 and diff.days < 365:
			months= math.floor(diff.days/30)
			if months == 1:
				return str(months) + " month ago"
			else:
				return str(months) + " months ago"
		if diff.days >= 365:
			years= math.floor(diff.days/365)
			if years == 1:
				return str(years) + " year ago"
			else:
				return str(years) + " years ago"	

class Reserve(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reserves')
	amount = models.PositiveIntegerField()

	def __str__(self):
		return "%s: %s" % (self.user.username, str(self.event))


class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.user)


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
	if kwargs.get('created', False):
		Profile.objects.get_or_create(user= kwargs.get('instance'),)