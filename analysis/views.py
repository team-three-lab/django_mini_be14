from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import get_object_or_404

from .models import Analysis
from .serializers import AnalysisSerializer
from .services import compute_analysis_data


class AnalysisListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        analyses = Analysis.objects.filter(user=request.user).order_by("-created_at")
        serializer = AnalysisSerializer(analyses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AnalysisSerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AnalysisDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return get_object_or_404(Analysis, pk=pk, user=request.user)

    def get(self, request, pk):
        analysis = self.get_object(request, pk)
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        analysis = self.get_object(request, pk)
        serializer = AnalysisSerializer(
            analysis,
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        analysis = self.get_object(request, pk)
        analysis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AnalysisResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return get_object_or_404(Analysis, pk=pk, user=request.user)

    def get(self, request, pk):
        analysis = self.get_object(request, pk)
        data = compute_analysis_data(analysis)
        return Response(data, status=200)