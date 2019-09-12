

from rest_framework import serializers
from django.contrib.auth.models import User

from events.models import Event, Reserve

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username']

class EventSerializer(serializers.ModelSerializer):
	organizer = UserSerializer()
	class Meta:
		model = Event
		fields = ['organizer', 'title', 'datetime', 'seats', 'location', 'description', 'picture']


class CreateEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ['title', 'datetime', 'seats', 'location', 'description', 'picture']

class ReserveSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	event = EventSerializer()
#	bookings = serializers.SerializerMethodField()
	class Meta:
		model = Reserve
		fields = ['user', 'event', 'amount']
	#def get_bookings(self,obj):
	#	bookings = Reserve.objects.filter(user=obj.user)
	#	return ReserveSerializer(bookings, many=True).data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        return validated_data
'''
class ReserveCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reserve
		fields = ['amount']
'''
'''
class ReserveseCreateSerializer(serializers.Serializer):
	user = serializers.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
	event = serializers.ForeignKey(Event, on_delete=models.CASCADE, related_name='reserves')
	amount = serializers.PositiveIntegerField()

	def create(self, validated_data):
		return Reserve.objects.create(**validated_data)
'''