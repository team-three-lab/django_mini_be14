from rest_framework import serializers
from .models import Notification

"""
요구사항

1. 알람 조회 : 전체 알람 조회

2. 알람 수정 : 읽음 여부의 false 값이 true로 바뀌는 수정

3. 알람 세부 조회 : analysis로 redirect

4. 알람 삭제  : 알람을 유저가 직접 삭제

"""

class NotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        # id는 삭제하거나 상세 조회할 때 필요하다고 해서 넣었습니다.
        # is_read가 프론트엔드에서 '읽음 알림'을 흐리게 표시하기 위해 필요하다고 합니다.
        # 근데 저는 잘 모르겠어서 
        fields = [
            'id',
            'message',
            'is_read',
            'created_at'
        ]

class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'is_read'
        ]

