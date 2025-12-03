from django.urls import path
from .views import AnalysisListCreateView, AnalysisDetailView, AnalysisResultView

urlpatterns = [
    path("", AnalysisListCreateView.as_view()),
    path("<int:pk>/", AnalysisDetailView.as_view()),
    path("<int:pk>/result/", AnalysisResultView.as_view())
]
