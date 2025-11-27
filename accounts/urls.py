from django.urls import path
from .views import AccountListCreateView, AccountRetrieveUpdateDestroyView

urlpatterns = [
    path('', AccountListCreateView.as_view()),
    path('<int:pk>/', AccountRetrieveUpdateDestroyView.as_view()),
]