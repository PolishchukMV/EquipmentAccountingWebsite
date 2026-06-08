"""
URL-маршруты для приложения обратной связи.
"""

from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.FeedbackListView.as_view(), name='feedback_list'),
    path('create/', views.FeedbackCreateView.as_view(), name='feedback_create'),
    path('<int:pk>/', views.FeedbackDetailView.as_view(), name='feedback_detail'),
    path('<int:pk>/respond/', views.FeedbackRespondView.as_view(), name='feedback_respond'),
    path('<int:pk>/status/', views.FeedbackStatusView.as_view(), name='feedback_status'),
]