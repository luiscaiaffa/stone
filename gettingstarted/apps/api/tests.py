from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from gettingstarted.apps.wallet.models import CreditCard, Wallet, Invoice
from .serializers import CreditCardSerializer, WalletSerializer, WalletUpdateSerializer, InvoiceSerializer, InvoiceUpdateSerializer


# Credit card
class CreateListCardTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.data = {
            "number": "4242424242424242",
            "due_date": 15,
            "credit_limit": 500,
            "exp_year": 18,
            "name": "CARTAO TESTE",
            "verification_value": "123",
            "exp_month": 12
        }

    def test_can_create_card(self):
        response = self.client.post(reverse('card'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_read_card_list(self):
        response = self.client.get(reverse('card'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateListCardTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.card = CreditCard.objects.create(
            number="4242424242424241", 
            due_date=15,
            credit_limit=500,
            exp_year=18,
            name="CARTAO TESTE",
            verification_value="123",
            exp_month=12,
            user= self.superuser,
        )
        self.data = CreditCardSerializer(self.card).data
        self.data.update({'credit_limit': 600})
        

    def test_can_update_wallet(self):
        response = self.client.put(reverse('card-detail', args=[self.card.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# End Credit card


# Wallet
class CreateListWalletTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.card = CreditCard.objects.create(
            number="4242424242424241", 
            due_date=15,
            credit_limit=500,
            exp_year=18,
            name="CARTAO TESTE",
            verification_value="123",
            exp_month=12,
            user= self.superuser,
        )
        self.data = {
            "cards": [
                self.card.id
            ],
            "limit": 200
        }
    
    def test_can_create_wallet(self):
        response = self.client.post(reverse('wallet'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

    def test_can_read_wallet_list(self):
        response = self.client.get(reverse('wallet'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateListWalletTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.card = CreditCard.objects.create(
            number="4242424242424241", 
            due_date=15,
            credit_limit=500,
            exp_year=18,
            name="CARTAO TESTE",
            verification_value="123",
            exp_month=12,
            user= self.superuser,
        )
        self.wallet = Wallet.objects.create(
            limit=100, 
            user= self.superuser,
        )
        self.wallet.cards.add(self.card.id)
        self.data = WalletSerializer(self.wallet).data
        self.data.update({'limit': 200})
        

    def test_can_update_wallet(self):
        response = self.client.put(reverse('wallet-detail', args=[self.wallet.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# End Wallet


# Invoice
class ListInvoiceTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_can_read_invoice_list(self):
        response = self.client.get(reverse('invoice'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# End Invoice