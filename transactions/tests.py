from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from accounts.models import Account
from transactions.models import Transaction


User = get_user_model()


class TransactionAPITestCase(APITestCase):

    def setUp(self):
        # ✅ create_user 안 쓰고 create()로 우회 (중요!!)
        self.user = User.objects.create(
            email="test@test.com",
            nickname="test",
            name="test user",
            phone_number="01011112222",
            password="1234"
        )
        self.user.set_password("1234")
        self.user.save()

        self.client.force_authenticate(user=self.user)

        self.account = Account.objects.create(
            user=self.user,
            account_name="테스트 계좌",
            balance=10000
        )

        self.base_url = reverse("transactions:list", args=[self.account.id])

    def test_get_transaction_list(self):
        Transaction.objects.create(
            account=self.account,
            amount=5000,
            description="편의점",
            is_deposit=False,
            transaction_type="CARD"
        )

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_transaction(self):
        data = {
            "amount": 3000,
            "description": "입금 테스트",
            "is_deposit": True,
            "transaction_type": "ATM"
        }

        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_transaction(self):
        transaction = Transaction.objects.create(
            account=self.account,
            amount=2000,
            description="치킨",
            is_deposit=False,
            transaction_type="CARD"
        )

        url = reverse("transactions:detail", args=[transaction.id])
        data = {"description": "피자"}

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "피자")

    def test_delete_transaction(self):
        transaction = Transaction.objects.create(
            account=self.account,
            amount=1000,
            description="삭제 테스트",
            is_deposit=False,
            transaction_type="CARD"
        )

        url = reverse("transactions:detail", args=[transaction.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
