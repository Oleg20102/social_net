from django.urls import path
from .views import home_view, profile_view, register_view, user_search

urlpatterns = [
    path('', home_view, name='home'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('register/', register_view, name='register'),

    path('search/', user_search, name='user_search'),
]
