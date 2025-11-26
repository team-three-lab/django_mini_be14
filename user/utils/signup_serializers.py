from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'nickname', 'name', 'phone_number']

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2', None)  # password2는 검증 후 제거 db에 저장 안함

        if password and password2 and password != password2: # 회원 정보 수정시 password2가 없는 상태기 때문에 이부분 패스
            raise serializers.ValidationError({
                "password2": ["두 비밀번호가 일치하지 않습니다."]
            })
        user = User(**data)
        errors = {}

        if 'password' in data:
            user = self.instance or User(**data)
            try:
                validate_password(password=data['password'], user=user)
            except ValidationError as e:
                errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return data


    def create(self, validated_data):
        user = User(**validated_data)

        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)

        if password:# 회원 정보 수정시 비번 해시화
            instance.set_password(password)
            instance.save()

        return instance