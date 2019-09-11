from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name="logintoken"),
    path('register/', views.Register.as_view(), name="register" ),
    path('events/upcoming/', views.UpcomingEventList.as_view(), name="upcoming-list" ),
    path('events/userlist/', views.UserEventsList.as_view(), name="user-list" ),
    path('events/create/', views.CreateEvent.as_view(), name="create-event" ),
    path('events/update/<int:event_id>/', views.UpdateEvent.as_view(), name="update-event" ),
    path('events/organizerlist/<int:event_id>/', views.OrganizerEventUserList.as_view(), name="organizer-list"),
    path('events/book/<int:event_id>/', views.CreateBook.as_view(), name = "create-book"),
    path('events/view/<int:organizer_id>/', views.OrganizerEventsList.as_view(), name = "view-events"),

]


