from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from accounts import views

appname = 'accounts'

urlpatterns = [
    #auth
    path("signup/", views.SignUpAPIView.as_view(), name="signup"),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    #jws
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]