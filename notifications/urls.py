from django.urls import path
from .views import NotificationList, NotificationRetrieveUpdateDestroyView

urlpatterns = [
    path('', NotificationList.as_view()),
    path('<int:pk>/', NotificationRetrieveUpdateDestroyView.as_view())
]