from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

from .models import Analysis
from .serializers import AnalysisSerializer
from transactions.models import Transaction


class AnalysisListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        analyses = Analysis.objects.filter(user=request.user).order_by("-created_at")
        serializer = AnalysisSerializer(instance=analyses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AnalysisSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AnalysisDetailView(APIView):
    """
    특정 Analysis 프리셋 하나에 대한 상세/수정/삭제
    GET    /api/analysis/<pk>/
    PUT    /api/analysis/<pk>/
    PATCH  /api/analysis/<pk>/
    DELETE /api/analysis/<pk>/
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        # 본인 소유만
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

    def patch(self, request, pk):
        analysis = self.get_object(request, pk)
        serializer = AnalysisSerializer(
            analysis,
            data=request.data,
            partial=True,
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
    """
    저장된 Analysis 설정을 기준으로,
    Transaction을 필터링해서 그래프용 데이터 뽑아주는 뷰.

    GET /api/analysis/<pk>/result/
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return get_object_or_404(Analysis, pk=pk, user=request.user)

    def get(self, request, pk):
        analysis = self.get_object(request, pk)
        qs = Transaction.objects.filter(
            account=analysis.account,
            is_deposit=analysis.is_income,
            transacted_at__range=(analysis.start_date, analysis.end_date),
        ).order_by("transacted_at")

        # A) 총합
        total_amount = sum(t.amount for t in qs)

        # B) 일자별 합계 (라인 차트)
        daily_chart = {}
        for t in qs:
            day = t.transacted_at.date().isoformat()
            daily_chart.setdefault(day, 0)
            daily_chart[day] += t.amount

        # 거래 타입별 합계 (파이 차트)
        type_chart = {}
        for t in qs:
            key = t.transaction_type  
            type_chart.setdefault(key, 0)
            type_chart[key] += t.amount

        # description 기반 카테고리 합계 (선택)
        description_chart = {}
        for t in qs:
            key = t.description or "기타"
            description_chart.setdefault(key, 0)
            description_chart[key] += t.amount


        data = {
            "analysis": {
                "id": analysis.id,
                "account": analysis.account.id,
                "is_income": analysis.is_income,
                "period": analysis.period,
                "start_date": analysis.start_date,
                "end_date": analysis.end_date,
            },
            "summary": {
                "total_amount": total_amount,
                "transactions_count": qs.count(),
            },
            "daily_chart": daily_chart,
            "type_chart": type_chart,
            "description_chart": description_chart,
        }

        return Response(data, status=status.HTTP_200_OK)