from django.test import TestCase
from faker import Faker
from user.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

fake = Faker('ko_KR')



# class UserModelTest(TestCase): # Faker로 유저 랜덤 생성
#     def create_random_users(count=10):
#         print(f" 유저 {count}명 생성을 시작합니다...")
#
#         for i in range(count):
#             try:
#                 # 1. 랜덤 데이터 생성
#                 email = fake.unique.email()  # 중복 없는 이메일
#                 nickname = fake.unique.user_name()  # 중복 없는 닉네임
#                 name = fake.name()  # 랜덤 이름 (예: 김철수)
#                 phone_number = fake.phone_number()  # 랜덤 전화번호 (예: 010-1234-5678)
#
#                 # 2. 유저 생성 (UserManager 사용)
#                 User.objects.create_user(
#                     email=email,
#                     nickname=nickname,
#                     password="password123!",
#                     name=name,
#                     phone_number=phone_number
#                 )
#             except Exception as e:
#                 print(f"❌ {i + 1}번째 유저 생성 실패: {e}")
#                 continue
#
#         print(f"✅ {count}명의 유저 생성이 완료되었습니다!")
#
#
#     # 실행 (예: 50명 만들기)
#     create_random_users(50)

'''
#테스트 코드는 assertEqual, assertIn으로 검증되는데 assertEqual은 같은지 assertIn은 포함되는지를 검증

# user_names = ["alice", "bob", "charlie"]
# self.assertIn("bob", user_names)  # 통과 (Pass)

# error_message = "Invalid username or password"
# self.assertIn("Invalid username", error_message)  # 통과 (Pass)
'''

User = get_user_model()

class UserAPITest(APITestCase):
    def setUp(self):### 테스트에 사용될 유저 정보 셋업 ###
        self.user_data = {
            "email": "test@api.com", "password": "strongpassword123!", "nickname": "apitestuser", "name": "API유저",
            "phone_number": "010-1234-5678"
        }
        self.user = User.objects.create_user(**self.user_data)

        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile', kwargs={'nickname': self.user.nickname})

        self.other_user = User.objects.create_user(
            email="other@test.com", nickname="otheruser", password="otherpassword", name="타인",
            phone_number="010-5555-5555"
        )

    def test_signup_success(self):### 회원가입 테스트 ###
        data = {"email": "new@test.com", "password": "password123!", "password2": "password123!", "nickname": "newuser",
                "name": "신규유저", "phone_number": "010-9999-9999"}
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_password_mismatch(self): ### 비번 불일치시 가입 실패 체스트###
        data = {"email": "fail@test.com", "password": "password123!", "password2": "different!", "nickname": "failuser",
                "name": "실패", "phone_number": "010-0000-0000"}
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self): ### JWT 토큰 획득 성공 테스트 ###
        data = {"email": self.user_data['email'], "password": self.user_data['password']}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_get_profile_authenticated(self): ### 본인 프로필 조회 테스트 ###
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_profile(self):### 회원 정보 수정 (본인) 테스트 ###
        self.client.force_authenticate(user=self.user)
        data = {"name": "수정된이름", "password": self.user_data['password'], "password2": self.user_data['password']}
        response = self.client.put(self.profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "수정된이름")

    def test_update_other_user_profile_fail(self):### 타인 프로필 수정 시도 실패 테스트 (권한 없음) ###
        self.client.force_authenticate(user=self.user)
        other_profile_url = reverse('profile', kwargs={'nickname': self.other_user.nickname})
        data = {"name": "해킹된이름"}
        response = self.client.put(other_profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_soft_delete_user(self):### 회원 탈퇴 (Soft Delete) 성공 테스트 ###
        self.client.force_authenticate(user=self.user)
        data = {"password": self.user_data['password']}
        response = self.client.delete(self.profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_soft_delete_wrong_password_fail(self):### 회원 탈퇴 시 비밀번호 불일치 실패 테스트 ###
        self.client.force_authenticate(user=self.user)
        data = {"password": "wrongpassword"}
        response = self.client.delete(self.profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_logout(self):### 로그아웃 (Refresh Token 블랙리스트) 테스트 ###
        # JWT 토큰 획득
        login_resp = self.client.post(self.login_url,
                                      {"email": self.user_data['email'], "password": self.user_data['password']})
        refresh_token = login_resp.data['refresh']

        # 로그아웃 요청
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.logout_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
