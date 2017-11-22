from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator


# Credit card
class CreditCard(models.Model):
    name = models.CharField(
        max_length=45, 
        help_text='Your name can be located by looking on your credit(EX: YOUR NAME)'
    )
    number = models.CharField(
        unique=True, 
        max_length=16, 
        help_text='Your number can be located by looking on your credit(EX: 4242424242424242)',
        validators= [MaxLengthValidator(16), MinLengthValidator(16)]
    )
    exp_month = models.IntegerField(
        help_text='Format MM (EX: 01, 12)',
        validators= [MaxValueValidator(12), MinValueValidator(1)]
    )
    exp_year = models.IntegerField(
        help_text='Format YY (EX: 17, 21)'
    )
    due_date = models.IntegerField(
        help_text='Format DD (EX: 01, 31)',
        validators= [MaxValueValidator(31), MinValueValidator(1)]
    )
    verification_value = models.CharField(
        max_length=4, 
        help_text='Your CVV number can be located by looking on your credit(EX: 123, 1234)',
        validators= [MaxLengthValidator(4), MinLengthValidator(3)]
    )
    credit_limit = models.DecimalField(
        max_digits=13, 
        decimal_places=2
    )
    invoice = models.DecimalField(
        max_digits=13, 
        decimal_places=2,
        default=0,
        help_text='Your invoice total',
    )
    balance = models.DecimalField(
        max_digits=13, 
        decimal_places=2,
        default=0,
        help_text='Your balance',
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Credit card"

    def __str__(self):
        return '{} {} {}'.format(self.name, self.due_date, self.balance)

    def save(self, *args, **kwargs):
        self.balance = self.credit_limit - self.invoice
        super(CreditCard, self).save(*args, **kwargs)
# End Credit card


# Wallet
class Wallet(models.Model):
    cards = models.ManyToManyField(
        CreditCard,
        help_text='Your credit cards of wallet',
    )
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )
    max_limit = models.DecimalField(
        max_digits=13, 
        decimal_places=2,
        default=0,
        help_text='Your maximum credit limit',
    )
    limit = models.DecimalField(
        max_digits=13, 
        decimal_places=2,
        default=0,
        help_text='Your credit limit',
    )
    credit = models.DecimalField(
        max_digits=13, 
        decimal_places=2,
        default=0,
        help_text='your total credit',
    )    

    class Meta:
        verbose_name = "Wallet"

    def __str__(self):
        return '{} {}'.format(self.user, self.credit)

def post_save_wallet(sender, instance, action, **kwargs):    
    if action == 'post_add' or action == 'post_remove':
        max_limit = instance.cards.all().aggregate(Sum('credit_limit'))['credit_limit__sum'] or 0
        invoice = instance.cards.all().aggregate(Sum('invoice'))['invoice__sum'] or 0
        instance.max_limit = max_limit
        instance.credit = max_limit - invoice
        instance.save()

m2m_changed.connect(post_save_wallet, sender=Wallet.cards.through)
# End Wallet

# Invoice
class Invoice(models.Model):
    description = models.CharField(
        max_length=45, 
        help_text='Description of your invoice'
    )
    price = models.DecimalField(
        max_digits=13, 
        decimal_places=2,
        default=0,
        help_text='Price',
    )
    due_date = models.DateField(
        help_text='Due date'
    )
    cards = models.ManyToManyField(
        CreditCard,
        related_name='invoice_credit_card',
        help_text='Credit cards of wallet',
        blank=True,
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    pay = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = "Invoice"

    def __str__(self):
        return '{} {}'.format(self.description, self.price)
# End Invoice