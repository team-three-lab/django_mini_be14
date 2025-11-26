from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from user.utils.signup_serializers import SignUpSerializer
from rest_framework.response import Response
from user.models import User

class SignUpAPIView(CreateAPIView):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LogoutAPIView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, nickname, *args, **kwargs):
        user = get_object_or_404(User, nickname=nickname)
        if user == request.user:
            serializer = SignUpSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"message": "로그인한 유저와 다릅니다."})

    def put(self, request, nickname, *args, **kwargs):
        user = get_object_or_404(User, nickname=nickname)
        if user == request.user:
            serializer = SignUpSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "수정 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        password = request.data.get('password')
        user = request.user
        if not user.check_password(password):
            return Response({"error": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        user.soft_delete()
        return Response({"message": "회원탈퇴에 성공했습니다."})