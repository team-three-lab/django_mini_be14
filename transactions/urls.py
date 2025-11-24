from django.urls import path
from .views import TransactionListCreateView
urlpatterns = [
 path("", TransactionListCreateView.as_view())   
]

from django.urls import path
from .views import TransactionListCreateView, TransactionDetailView

urlpatterns = [
    # /transactions/
    path("", TransactionListCreateView.as_view(), name="transaction-list"),

    # /transactions/1/
    path("<int:pk>/", TransactionDetailView.as_view(), name="transaction-detail"),
]
