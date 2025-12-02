from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['nickname'] = user.nickname
        token['email'] = user.email
        token['is_admin'] = user.is_admin

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data['nickname'] = self.user.nickname
        data['email'] = self.user.email
        data['is_admin'] = self.user.is_admin

        return data