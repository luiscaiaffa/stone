from decimal import Decimal
from datetime import datetime
from django.db.models import Sum
from rest_framework import serializers

from gettingstarted.apps.wallet.models import CreditCard, Wallet, Invoice


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


# Credit card
class CreditCardSerializer(DynamicFieldsModelSerializer):

    def validate(self, data):
        date = datetime.now()
        year = int(str(date.year)[2:])
        month = date.month  

        if int(data['exp_year']) < year:
            raise serializers.ValidationError("exp_year < year now")
        if int(data['exp_month']) < month and int(data['exp_year']) == year:
            raise serializers.ValidationError("exp_month < month now")
        if self.instance:
            if Wallet.objects.filter(cards=self.instance.pk):
                raise serializers.ValidationError("To edit a card, please remove it from the wallet!")

        return data

    class Meta:
        model = CreditCard
        fields = '__all__'
        read_only_fields = ('invoice', 'user', 'balance', )
# End Credit card


# Wallet
class WalletSerializer(DynamicFieldsModelSerializer):

    def validate(self, data):
        limit = Decimal(0.00)
        for card in data['cards']:
            limit += card.credit_limit
        
        if limit < data['limit']:
            raise serializers.ValidationError("Limit greater than the maximum limit")
        if Wallet.objects.filter(user=self.context['request'].user):
            raise serializers.ValidationError("You already have a wallet")

        return data
    
    class Meta:
        model = Wallet
        exclude = ('user',)
        read_only_fields = ('max_limit', 'credit',)
    

class WalletUpdateSerializer(DynamicFieldsModelSerializer):

    def validate(self, data):
        limit = Decimal(0.00)
        for card in data['cards']:
            limit += card.credit_limit
        
        if limit < data['limit']:
            raise serializers.ValidationError("Attention! new limit, limit greater than the maximum limit")

        return data
    
    class Meta:
        model = Wallet
        exclude = ('user',)
        read_only_fields = ('max_limit', 'credit',)
# End Wallet


# Invoice
class InvoiceSerializer(DynamicFieldsModelSerializer):

    def validate(self, data):
        credit = Wallet.objects.get(user=self.context['request'].user).credit
        if credit < data['price']:
            raise serializers.ValidationError("Price greater than the credit")
        
        return data

    class Meta:
        model = Invoice
        exclude = ('user',)
        read_only_fields = ('cards',)


class InvoiceUpdateSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Invoice
        exclude = ('user',)
        read_only_fields = ('cards', 'due_date', 'description',)
# End Invoice