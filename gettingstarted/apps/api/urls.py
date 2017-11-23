from gettingstarted.apps.api import views
from django.conf.urls import url

urlpatterns = [
    # Card
    url(r'^card/$', views.CreditCardList.as_view(), name='card'),
    url(r'^card/(?P<pk>[0-9]+)$', views.CreditCardDetail.as_view(), name='card-detail'),
    # Wallet
    url(r'^wallet/$', views.WalletList.as_view(), name='wallet'),
    url(r'^wallet/(?P<pk>[0-9]+)$', views.WalletDetail.as_view(), name='wallet-detail'),
    # Invoice
    url(r'^invoice/$', views.InvoiceList.as_view(), name='invoice'),
    url(r'^invoice/(?P<pk>[0-9]+)/pay/$', views.InvoiceDetail.as_view(), name='invoice-detail'),
]
