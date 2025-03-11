from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register, name='register'),
    path('vote/', views.vote, name='vote'),
    path('voted/', views.voted, name='voted'),
    path('review/', views.review, name='review'),
    path('positions-list/', views.positions_list, name='positions_list'),
    path('voting-status/', views.voting_status, name='voting_status'),
    path('spoiled-votes/', views.spoiled_votes, name='spoiled_votes'),
    path('position-details/<int:position_id>/', views.position_details, name='position_details'),  # New URL pattern
]

