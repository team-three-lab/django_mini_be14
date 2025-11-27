from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):

    user = models.ForeignKey(User,verbose_name='회원 정보' ,on_delete=models.CASCADE)
    message = models.TextField('알람 메세지 내용')
    is_read = models.BooleanField('읽음 여부', default=False)
    created_at = models.DateTimeField('알람 생성 날짜', auto_now_add=True)

    def __str__(self):
        status = "[읽음]" if self.is_read else "[안읽음]"
        return f"{status} {self.message[:10]}..."
    
    class Meta:
        verbose_name = "알림"
        verbose_name_plural = "알림 목록"
        ordering = ['-created_at']
