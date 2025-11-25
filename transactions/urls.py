from django.urls import path
from .views import TransactionListCreateView, TransactionRetrieveUpdateDestroyViewView

urlpatterns = [
    path("", TransactionListCreateView.as_view()),
    path("<int:pk>/", TransactionRetrieveUpdateDestroyViewView.as_view())
]