from django.urls import path

from .views import UserDetailViews, UserViews

urlpatterns = [
    path("users/", UserViews.as_view()),
    path("users/<str:username>", UserDetailViews.as_view()),
]
