from django.conf.urls                   import url
from django.urls                        import path

from .                                  import views

from wenjian.views                      import JobList, NewJob, LoginView, LogoutView
from wenjian.views                      import PortList, PortNew, PortUpdate
from wenjian.views                      import CurrencyNew, CurrencyUpdate, CurrencyList
from wenjian.views                      import RoleNew, RoleUpdate, RoleList
from wenjian.views                      import ClientNew, ClientList, ClientRole
from wenjian.views                      import ContactNew, ContactUpdate, ContactList
from wenjian.views                      import ExpenseList, ExpenseNew, ExpenseUpdate
from wenjian.views                      import ContainersizeNew, ContainersizeUpdate, ContainersizeList
from wenjian.views                      import BranchOffice, UpdateOffice, BranchOfficeList
from wenjian.views                      import User, UserList, ChangePassword, UpdateUser
from wenjian.views                      import CntrListView, ContainerView


urlpatterns = [
    url(r'^$',                          views.home,                     name='home'),

    # Login and Logout
    path('login/',                      LoginView.as_view(),            name = 'login'),
    path('logout/',                     views.LogoutView,               name = 'logout'),

    # USER urls
    path('userlist/',                   UserList.as_view(),             name = 'userlist'),
    path('user/',                       User.as_view(),                 name = 'newuser'),
    path('user/<pk>',                   UpdateUser.as_view(),           name = 'updateuser'),
    path('password/<pk>',               ChangePassword.as_view(),       name = 'password'),    

    # Branch Office urls
    path('branchoffice/',               BranchOffice.as_view(),         name = 'newoffice'),
    path('branchoffice/<pk>',           UpdateOffice.as_view(),         name = 'updateoffice'),
    path('officelist/',                 BranchOfficeList.as_view(),     name = 'officelist'),


    # Job Handling url List
    path('joblist/',                    JobList.as_view(),              name = 'joblist'),
    path('job/',                        NewJob.as_view(),               name = 'newjob'),
    path('job/<pk>',                    NewJob.as_view(),               name = 'updatejob'),
    
    path('containerlist/<job_no>',      CntrListView.as_view(),         name = 'containerlist'),
    path('container/<job_no>',          ContainerView.as_view(),        name = 'newcontainer'),
    path('containerupdt/<pk>',          ContainerView.as_view(),        name = 'updatecontainer'),

    # Client url list
    path('client/',                     ClientNew.as_view(),            name = 'client'),
    path('client/<pk>',                 ClientNew.as_view(),            name = 'clientupdate'),
    path('clientlist/<page_id>',        ClientList.as_view(),           name = 'clientlist'),

    # Contact url List
    path('contactlist/<client_id>',     ContactList.as_view(),          name = 'contactlist'),
    path('contactadd/<client_id>',      ContactNew.as_view(),           name = 'contactadd'),
    path('contact/<pk>',                ContactUpdate.as_view(),        name = 'contactupdate'),

    # Client Roles url
    path('clientrole/<client_id>',     ClientRole.as_view(),            name = 'clientrole'),

    # port handling url list
    path('portlist/',                   PortList.as_view(),             name = 'portlist'),
    path('port/',                       PortNew.as_view(),              name = 'port'),
    path('port/<pk>',                   PortUpdate.as_view(),           name = 'portupdate'),

    # currency handling url list
    path('currency/',                   CurrencyNew.as_view(),          name = 'currency'),
    path('currency/<pk>',               CurrencyUpdate.as_view(),       name = 'currency_update'),
    path('currencylist',                CurrencyList.as_view(),         name = 'currencylist'),

    # role handling url list
    path('role/',                       RoleNew.as_view(),              name = 'role'),
    path('role/<pk>',                   RoleUpdate.as_view(),           name = 'roleupdate'),
    path('rolelist/',                   RoleList.as_view(),             name = 'rolelist'),

    # expense handling url list
    path('expense/',                    ExpenseNew.as_view(),           name = 'expense'),
    path('expense/<pk>',                ExpenseUpdate.as_view(),        name = 'expenseupdate'),
    path('expenselist/',                ExpenseList.as_view(),          name = 'expenselist'),

    # ContainerSize handling url list
    path('containersize/',              ContainersizeNew.as_view(),     name = 'containersize'),
    path('containersize/<pk>',          ContainersizeUpdate.as_view(),  name = 'containersizeupdate'),
    path('containersizelist/',          ContainersizeList.as_view(),    name = 'containersizelist'),
]