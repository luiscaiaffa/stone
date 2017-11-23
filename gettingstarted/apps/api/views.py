from decimal import Decimal
from rest_condition import Or
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import generics, filters, pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication

from gettingstarted.apps.wallet.models import CreditCard, Wallet, Invoice
from .serializers import CreditCardSerializer, WalletSerializer, WalletUpdateSerializer, InvoiceSerializer, InvoiceUpdateSerializer


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'pagination': {
                'actual_page': self.page.number,
                'last_page': self.page.paginator.num_pages,
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
                'start_index': self.page.start_index(),
                'end_index': self.page.end_index(),
            },
            'results': data
        })


class CustomList(object):
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    filter_fields = '__all__'
    ordering_fields = '__all__'
    pagination_class = CustomPagination


# Credit card
class CreditCardList(CustomList,generics.ListCreateAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    ordering = 'id'
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]

    def get_queryset(self):
        user = self.request.user
        return CreditCard.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreditCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if Wallet.objects.filter(cards=instance.pk):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"non_field_errors": ["To delete a card, please remove it from the wallet!"]})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
# End Credit card


# Wallet
class WalletList(CustomList,generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    ordering = 'id'
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WalletDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletUpdateSerializer
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]
# End Wallet


# Invoice
def filter_wallet(day, price, user, instance):
    value = Decimal(0.00)
    price = Decimal(price)
    wallet = Wallet.objects.get(user=user)
    cards = wallet.cards.all().filter(due_date__gt=day, invoice=0).order_by('-due_date', 'credit_limit')
    wallet.credit = wallet.credit - price
    wallet.save()
    for card in cards:
        if card.balance >= price:
            value  = card.balance - price
            card.balance = value
            card.invoice = price
            card.save()
            instance.cards.add(card)
            break
        else:
            price = price - card.balance
            card.invoice = card.balance
            card.balance = 0
            card.save()
            instance.cards.add(card)
    

class InvoiceList(CustomList,generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    ordering = 'id'
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]

    def perform_create(self, serializer):
        user = self.request.user
        instance = serializer.save(user=user)
        data = serializer.data
        day = int(data['due_date'].split('-')[-1])
        price = data['price']
        filter_wallet(day, price, user, instance)


class InvoiceDetail(APIView):
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [Or(IsAdminUser, TokenHasReadWriteScope)]
    
    def get_object(self, pk):
        try:
            return Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            raise Http404
   
    def get(self, request, pk, format=None):
        value = self.get_object(pk)
        serializer = InvoiceSerializer(value)
        return Response(serializer.data)
    
    def patch(self, request, pk, format=None):
        value = self.get_object(pk)
        serializer = InvoiceUpdateSerializer(value, data=request.data)
        if serializer.is_valid():
            serializer.save()
            wallet = wallet = Wallet.objects.get(user=self.request.user)
            wallet.credit = wallet.credit + value.price
            wallet.save()
            for card in value.cards.all():
                card.invoice = 0
                card.balance = card.credit_limit
                card.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# End Invoice
