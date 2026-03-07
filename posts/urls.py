from django.urls import path
from . import views

urlpatterns = [
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("like/<int:post_id>/", views.toggle_like, name="toggle_like"),
]
