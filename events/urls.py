

from django.urls import path
from . import views
from API import views as api
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
	path('', views.home, name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('events/', views.event_list, name='event-list'),
    path('dashboard/', views.my_event_list, name='dashboard'),
    path('events/detail/<int:event_id>/', views.event_detail, name='event-detail'),
    path('events/create', views.event_create, name='event-create'),
    path('events/<int:event_id>/update/', views.event_update, name='event-update'),
    path('events/<int:event_id>/book/', views.event_book, name='event-book'),
    path('prevevents/', views.prev_event, name='prev-events'),

    path('token/', TokenObtainPairView.as_view(), name="login"),
    path('register/', api.Register.as_view(), name="register" ),
    path('events/upcoming/', api.UpcomingEventList.as_view(), name="upcoming-list" ),
    path('events/userlist/', api.UserEventsList.as_view(), name="user-list" ),
    path('events/create/', api.CreateEvent.as_view(), name="create-event" ),
    path('events/update/<int:event_id>/', api.UpdateEvent.as_view(), name="update-event" ),
    path('events/organizerlist/<int:event_id>/',api.OrganizerEventUserList.as_view(), name="organizer-list"),
    path('events/book/<int:event_id>/',api.CreateBook.as_view(), name = "create-book"),
    path('events/view/<int:organizer_id>/',api.OrganizerEventsList.as_view(), name = "view-events"),

    
   
]