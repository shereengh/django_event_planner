from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
	path('', views.home, name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('',include('API.urls')),
    path('events/', views.event_list, name='event-list'),
    path('dashboard/', views.my_event_list, name='dashboard'),
    path('events/detail/<int:event_id>/', views.event_detail, name='event-detail'),
    path('events/create', views.event_create, name='event-create'),
    path('events/<int:event_id>/update/', views.event_update, name='event-update'),
    path('events/<int:event_id>/book/', views.event_book, name='event-book'),
    path('prevevents/', views.prev_event, name='prev-events'),
    path('events/myevents/',views.bookingslist, name='my-bookings'),
    path('events/<int:reserve_id>/cancel/', views.cancel_booking, name='cancel-booking'),
    path('profile/<int:user_id>/', views.view_profile, name='profile'),
    path('profile/update/<int:user_id>/', views.profile_update, name='profile-update'),
]