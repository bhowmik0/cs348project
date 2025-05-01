from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('edit/<int:pk>/', views.event_edit, name='event_edit'),
    path('delete/<int:pk>/', views.event_delete, name='event_delete'),
    path('dishes/', views.dish_signup_list, name='dish_signup_list'),
    path('dishes/create/', views.dish_signup_create, name='dish_signup_create'),
    path('dishes/create/<int:event_id>/', views.dish_signup_create, name='dish_signup_create_with_event'),
    path('dishes/event/<int:event_id>/', views.dish_signups_for_event, name='dish_signups_for_event'),
    path('report/', views.event_report, name='event_report'),

]
