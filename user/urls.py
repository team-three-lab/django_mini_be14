from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from user import views

appname = 'user'

urlpatterns = [
    #auth
    path("signup/", views.SignUpAPIView.as_view(), name="signup"),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('login/<str:nickname>/', views.UserProfileView.as_view(), name='profile'),
    #jws
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]