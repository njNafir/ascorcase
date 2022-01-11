from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('create/', RestaurantAPIView.as_view()),
    re_path('update/(?P<pk>\d+)/', RestaurantUpdateAPIView.as_view()),
    path('create-menu/', MenuAPIView.as_view()),
    re_path('update-menu/(?P<pk>\d+)/', MenuUpdateAPIView.as_view()),
    path('current-day-menu/', TodaysMenuAPIView.as_view()),
    path('vote-menu/', VoteAPIView.as_view()),
    path('vote-result/', CurrentDayWinnerAPIView.as_view())
]
