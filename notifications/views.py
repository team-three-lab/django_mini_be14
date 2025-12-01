from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAccountOwner
# permissions accounts 폴더에 있는 permissions 파일 복사 했습니다.
from django.shortcuts import get_object_or_404, redirect

from .models import Notification
from .serializers import NotificationListSerializer, NotificationUpdateSerializer

class NotificationList(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # is_read=False로 하면 남의 알람까지 다 보인다고 해서 user=request.user로 바꿨습니다.
        notifications = Notification.objects.filter(
            # user=request.user
            ).order_by('-created_at')
        serializer = NotificationListSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# views.py 부분은 잘 모르겠어서 AI의 힘을 많이 빌렸습니다;;
# 이해할 수 있도록 노력하겠습니다.

class NotificationRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        # permission_classes = [IsAuthenticated, IsAccountOwner]
        # analysis의 detail로 redirect

        notification = get_object_or_404(Notification, pk=pk)
        self.check_object_permissions(request, Notification)

        if not notification.is_read:
            notification.is_read = True
            notification.save()

        return Response(status=status.HTTP_200_OK)

    
    def put(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        self.check_object_permissions(request, notification)

        serializer = NotificationUpdateSerializer(
            notification, 
            data=request.data, 
            partial=True 
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        self.check_object_permissions(request, notification)

        notification.delete()
        return Response(
            {
                "message": "알람이 삭제되었습니다."
            }, status=status.HTTP_200_OK)
