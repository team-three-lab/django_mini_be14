from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from user import views

appname = 'user'

urlpatterns = [
    #auth
    path("signup/", views.SignUpAPIView.as_view(), name="signup"), # 이거 왜 필수값이 phone_num만으로 한건지 궁금.
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    #jws
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), # 토큰 유효성 검사를 왜 넣었는지 궁금스

]