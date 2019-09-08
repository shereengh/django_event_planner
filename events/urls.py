from django.urls import path
from . import views
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
   # path('events/<int:event_id>/book/', views.event_book, name='event-book'),
   
]