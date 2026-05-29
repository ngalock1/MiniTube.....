from django.urls import path
from .views import MeView, ChannelView

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('channel/<int:pk>/', ChannelView.as_view(), name='channel-detail'),
]
