from django.conf.urls import url
from . import views
# from name_view import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    
    # Below is my own pages
    url(r'^payee/$', views.payeelist, name='payee'),
    url(r'^payee/(?P<payee_id>[0-9]+)/$', views.payeedetail, name='payeedetail'),
    url(r'^savepayee/(?P<payee_id>[0-9]+)/$', views.savepayee, name='savepayee'),

    #expenses
    url(r'^expense/$', views.expense, name='expense'),
    url(r'^expensedetail/(?P<expense_id>[0-9]+)/$', views.expensedetail, name='expensedetail'),

    url(r'^payment/$', views.payment, name='payment'),
    url(r'^chaxun/(?P<year_id>[0-9]+)$', views.chaxun, name='chaxun'),
    url(r'^pmtdtl/(?P<payee_id>[0-9]+)/(?P<year_id>[0-9]+)$', views.pmtdtl, name='pmtdtl'),
]