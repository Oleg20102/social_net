from django.urls import path
from . import views
from django.urls import path
from . import views



urlpatterns = [
    path("", views.group_list, name="group_list"),
    path("create/", views.create_group, name="create_group"),
    path("<slug:slug>/", views.group_detail, name="group_detail"),
    path("<slug:slug>/join/", views.join_group, name="join_group"),
    path("<slug:slug>/leave/", views.leave_group, name="leave_group"),
    path("<int:pk>/", views.group_detail, name="group_detail"),
    path("delete/<slug:slug>/", views.delete_group, name="delete_group"),
]