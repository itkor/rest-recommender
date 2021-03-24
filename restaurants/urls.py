from django.urls import path
from .views import (Search, RestaurantDetailView, RestaurantResultView, about, contact)

urlpatterns = [
	path('search/', Search.as_view(), name='search'),
	path('result/', RestaurantResultView.as_view(), name='result'),
	path('detail/<int:restaurant_id>', RestaurantDetailView.as_view(), name='detail'),
	path('about/', about, name='about'),
	path('contact/', contact, name='contact'),
]