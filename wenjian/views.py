from django.shortcuts               import render, get_object_or_404
from django.http                    import HttpResponse, HttpResponseRedirect
from django.utils                   import timezone
from django                         import forms
from django.urls                    import reverse
import datetime
from django.contrib.auth            import authenticate, login, logout
from django.contrib.auth.models     import User, Group
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.db.models               import Q

from django.views.generic.list      import ListView
from django.views.generic.base      import TemplateView, View, RedirectView
from django.views.generic.edit      import CreateView, FormView, UpdateView

# import models
from wenjian.models                 import client, client_pic, job, port, currency
from wenjian.models                 import role, client_role, expense, containersize, container
from wenjian.models                 import branch_user, branch_office, container

# import forms
from wenjian.forms                  import job_form, client_form, LoginForm
from wenjian.forms                  import PortForm, RoleForm, CurrencyForm, OfficeForm

from wenjian.forms                  import client_list_form, ExpenseForm
from wenjian.forms                  import contact_form, ContainersizeForm
from wenjian.forms                  import UserForm, UserUpdateForm, ContainerForm

from wenjian.classgrp               import CreateNewJob

def home(request):
    return render(request, 'wenjian/login.html')

class LoginView(View):
    form_class                  = LoginForm
    template_name               = 'wenjian/login.html'

    def get(self, request):
        form                    = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *arge, **kwargs):
        form = self.form_class(data = request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']            
            user = authenticate(username=username, password = password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    redirect_url = request.GET.get('next')
                    print(request.user.username)
                    if redirect_url:
                        return HttpResponseRedirect(redirect_url)
                    else:
                        return HttpResponseRedirect(reverse('joblist'))
        return HttpResponse("not login")

"""LOGOUT View"""
def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


"""Branch Office View"""
class BranchOffice(CreateView):
    model               = branch_office
    template_name       = 'wenjian/office.html'
    form_class          = OfficeForm


class UpdateOffice(UpdateView):
    model               = branch_office
    template_name       = 'wenjian/office.html'
    form_class          = OfficeForm


class BranchOfficeList(LoginRequiredMixin, ListView):
    login_url = 'login'

    model               = branch_office
    template_name       = 'wenjian/officelist.html'
    context_object_name = 'office_list'
    queryset            = branch_office.objects.all().order_by('office_shortcut')

"""CLIENT views"""
class ClientNew(View):
    template_name               = 'wenjian/client.html'
    form_class                  = client_form

    def get(self, request, *args, **kwargs):
        if self.kwargs:
            p=self.kwargs['pk']
            initial_data = get_object_or_404(client, pk=p)
            form = self.form_class(instance=initial_data)
        else:
            form = self.form_class()
            p = 0
        return render(request, self.template_name, { 'form': form, 'p' : p})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            if self.kwargs:
                pk = self.kwargs['pk']
                update_client = get_object_or_404(client, pk=pk)
                update_client.client_shortcut   = form.cleaned_data['client_shortcut'].upper()
                update_client.client_name       = form.cleaned_data['client_name'].upper()
                update_client.client_address    = form.cleaned_data['client_address'].upper()
                update_client.client_tel        = form.cleaned_data['client_tel']
                update_client.client_email      = form.cleaned_data['client_email'].lower()
                update_client.save()
            else:
                new_client = client(
                    client_shortcut             = form.cleaned_data['client_shortcut'].upper(),
                    client_name                 = form.cleaned_data['client_name'].upper(),
                    client_address              = form.cleaned_data['client_address'].upper(),
                    client_tel                  = form.cleaned_data['client_tel'],
                    client_email                = form.cleaned_data['client_email'].lower(),
                )
                new_client.save()
                new_client = client.objects.all().last()
                pk = new_client.id

            return HttpResponseRedirect(reverse('clientupdate', args=[pk]))


class ClientList(LoginRequiredMixin, View):
    login_url = 'login'
    template_name       = 'wenjian/clientlist.html'
    form = client_list_form()

    def get(self, request, *args, **kwargs):
        page_no = self.kwargs['page_id']
        queryset = client.objects.all().order_by('client_name')[(int(page_no)-1)*9 : int(page_no)*9]
        if queryset: 
            pass
        else:
            page_no = int(page_no) - 1
            queryset = client.objects.all().order_by('client_name')[(int(page_no)-1)*9 : int(page_no)*9]
            print(page_no)

        return render(request, self.template_name, {
            'form'          : self.form,
            'queryset'      : queryset,
            'page_no'       : page_no
        })

    def post(self, request, *args, **kwargs):
        if 'selected_client' in request.POST:
            s = self.request.POST.get('client_select')
            return HttpResponse('selected-client' + ':==' + str(s))
        # SEARCH button clicked #
        if 'search_content' in request.POST:
            page_no = self.kwargs['page_id']
            search_input = request.POST.get('search_content').upper()
            queryset = client.objects.filter(client_name__contains = search_input)
            return render(request, self.template_name, {
                'form'          : self.form,
                'queryset'      : queryset,
                'page_no'       : page_no
            })

"""Contact Person View List"""
class ContactNew(View):
    template_name       = 'wenjian/contact.html'
    form_class          = contact_form

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['client_id']
        form = self.form_class()
        pic                 = get_object_or_404(client_pic, pk=pk)
        selected_client     = pic.client
        return render(request, self.template_name, {
            'form':form,
            'client': selected_client,
            'pk': pk,
        })
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['client_id']

        form = contact_form(request.POST)
        if form.is_valid():
            new_contact = client_pic(client_id      = pk, 
                                     pic_name       = form.cleaned_data['pic_name'].upper(), 
                                     pic_mobile     = form.cleaned_data['pic_mobile'], 
                                     pic_email      = form.cleaned_data['pic_email'])
            new_contact.save()
        return HttpResponseRedirect(reverse('contactlist', args = pk))  # Redirect to list of contact

class ContactUpdate(View):   
    form_class          = contact_form
    template_name       = 'wenjian/contact.html'

    def get(self, request, *args, **kwargs):
        pic_id              = self.kwargs['pk']
        if pic_id == 0:
            return HttpResponse("new contact")
        else: 
            pic                 = get_object_or_404(client_pic, pk=pic_id)
            selected_client     = pic.client
            pk                  = pic.client_id
            form                = self.form_class(instance=pic)

        return render(request, self.template_name, {
            'form': form,
            'client': selected_client,
            'pk': pk,
        })
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        form = contact_form(request.POST)
        if form.is_valid():
            update_contact = get_object_or_404(client_pic, pk=pk)
            update_contact.pic_name       = form.cleaned_data['pic_name'].upper()
            update_contact.pic_mobile     = form.cleaned_data['pic_mobile']
            update_contact.pic_email      = form.cleaned_data['pic_email']
            update_contact.save()
        client_id = client_pic.objects.get(pk=pk).client_id
        return HttpResponseRedirect(reverse('contactlist', args=[client_id]))

class ContactList(View):
    template_name       = 'wenjian/contactlist.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['client_id']
        queryset = client_pic.objects.all().order_by('pic_name').filter(client = pk )
        selected_client = select_client(pk)

        return render(request, self.template_name, {
                'contact_list'  : queryset,
                'pk'            : pk,
                'client'        : selected_client
            })


class ClientRole(LoginRequiredMixin, View):
    login_url = 'login'
    
    template_name = 'wenjian/clientrole.html'

    def get(self, request, *args, **kwargs):
        pk                      = self.kwargs['client_id']
        selected_client         = select_client(pk)
        all_role                = role.objects.all()
        the_client_role         = client_role.objects.all().filter(client_id = pk)
        client_role_array       = []
        if the_client_role:
            for tcr in the_client_role:
                client_role_array.append(tcr.role.id)

        # 如果不够3行显示，凑够数的数字        
        c=[]
        role_counter = role.objects.count()%3
        if role_counter !=0:
            c=list(range(3-role_counter))

        return render(request, self.template_name, {
            'pk'                : pk,
            'all_role'          : all_role,
            'client_role'       : client_role_array,
            'c'                 : c,
            'client'            : selected_client,
        })
    
    def post(self, request, *args, **kwargs):
        the_client_id = self.kwargs['client_id']

        if 'role_select' in self.request.POST:
            client_old_role = client_role.objects.filter(client_id = the_client_id)
            old_role_id = []
            for r in client_old_role:
                old_role_id.append(r.role_id)

            roleselect = self.request.POST.getlist('role_select')
            for i in roleselect:
                if int(i) in old_role_id:
                    pass
                else:
                    client_new_role = client_role(
                            client_id   = the_client_id,
                            role_id     = i,
                        )
                    client_new_role.save()
            return HttpResponseRedirect(reverse('clientrole', args=[the_client_id]))
        else:
            return HttpResponse("Nothing select")

"""End of Client"""


"""JOB views"""
class JobList(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'wenjian/joblist.html'

    def get(self, request, *args, **kwargs):
        my_job          = CreateNewJob(request.user.username)
        my_id           = my_job.UserID()
        job_list        = job.objects.filter(Q(assistant_id=my_id)|Q(operator=my_id), status__exact='NORMAL')

        return render(request, self.template_name, {'job_list': job_list, })


"""NEW JOB View"""
class NewJob(LoginRequiredMixin, View):
    login_url           = 'login'

    template_name       = 'wenjian/newjob.html'
    form_class          = job_form

    def get(self, request, *args, **kwargs):
        my_new_job          = CreateNewJob(request.user.username)
        my_office_id        = my_new_job.Officeid()

        if self.kwargs:
            pk                              = self.kwargs['pk']
            init_job                        = job.objects.get(pk=self.kwargs['pk'])
            init_job_no                     = init_job.job_no
            form                            = self.form_class(instance = init_job)
        else:
            form                            = self.form_class(None)
            form.operator                   = my_new_job.UserID()
            init_job_no                     = ''
            pk                              = ''

        # Definite the select items Choice
        form.fields["client"]              .queryset = client.objects.filter(client_role__role_id = 2).order_by('client_shortcut')
        form.fields["book_agent"]          .queryset = client.objects.filter(client_role__role_id = 1).order_by('client_shortcut')
        form.fields["carrier"]             .queryset = client.objects.filter(client_role__role_id = 4).order_by('client_shortcut')
        form.fields["destination_agent"]   .queryset = client.objects.filter(client_role__role_id = 6).order_by('client_shortcut')
        form.fields["pol"]                 .queryset = port.objects.all().order_by('port')
        form.fields["pod"]                 .queryset = port.objects.all().order_by('port')      
        form.fields["operator"]            .queryset = branch_user.objects.filter(validate_date__gte=datetime.date.today(), 
                                                                                  branch_office__exact=my_office_id).order_by('username')      
        form.fields["assistant"]           .queryset = branch_user.objects.filter(validate_date__gte=datetime.date.today()).order_by('username')      

        return render(request, self.template_name, {'form': form, 'job_no': init_job_no, 'pk': pk,})

    def post(self, request, *args, **kwargs):
        form                                        = job_form(request.POST)
        
        if form.is_valid():
            if self.kwargs:
                pk                                  = self.kwargs['pk']
                update_job                          = job.objects.get(pk=pk)

                update_job.booking_no               = form.cleaned_data['booking_no']
                update_job.client                   = form.cleaned_data['client']
                update_job.carrier                  = form.cleaned_data['carrier']
                update_job.book_agent_id            = form.cleaned_data['book_agent']
                update_job.destination_agent_id     = form.cleaned_data['destination_agent']
                update_job.place_of_receipt         = form.cleaned_data['place_of_receipt']
                update_job.place_of_delivery        = form.cleaned_data['place_of_delivery']
                update_job.pol                      = form.cleaned_data['pol']
                update_job.pod                      = form.cleaned_data['pod']
                update_job.pre_carriage             = form.cleaned_data['pre_carriage']
                update_job.vessel                   = form.cleaned_data['vessel']
                update_job.voyage                   = form.cleaned_data['voyage'] 
                update_job.doc                      = form.cleaned_data['doc'] 
                update_job.etd                      = form.cleaned_data['etd'] 
                update_job.eta                      = form.cleaned_data['eta'] 
                update_job.status                   = form.cleaned_data['status'] 
                update_job.operator                 = form.cleaned_data['operator']
                update_job.assistant                = form.cleaned_data['assistant']
                
                update_job.save()
            else: 
                save_job            = CreateNewJob(request.user.username)
                save_job_no         = save_job.NewJobNo()

                new_job = job(
                    job_no                      = save_job_no, 
                    booking_no                  = form.cleaned_data['booking_no'],
                    client                      = form.cleaned_data['client'],
                    carrier                     = form.cleaned_data['carrier'],
                    book_agent                  = form.cleaned_data['book_agent'],
                    destination_agent           = form.cleaned_data['destination_agent'],
                    place_of_receipt            = form.cleaned_data['place_of_receipt'],
                    place_of_delivery           = form.cleaned_data['place_of_delivery'],
                    pol                         = form.cleaned_data['pol'],
                    pod                         = form.cleaned_data['pod'],
                    pre_carriage                = form.cleaned_data['pre_carriage'],
                    vessel                      = form.cleaned_data['vessel'],
                    voyage                      = form.cleaned_data['voyage'], 
                    doc                         = form.cleaned_data['doc'], 
                    etd                         = form.cleaned_data['etd'], 
                    eta                         = form.cleaned_data['eta'], 
                    create_date                 = datetime.date.today(), 
                    finish_date                 = form.cleaned_data['finish_date'], 
                    status                      = form.cleaned_data['status'], 
                    creator_id                  = int(save_job.UserID()),
                    operator                    = form.cleaned_data['operator'],
                    assistant                   = form.cleaned_data['assistant'],
                )
                new_job.save()
                pk                          = job.objects.get(job_no__exact=save_job_no).id
            
            return HttpResponseRedirect(reverse('updatejob', args=[pk]))
        else:
            msg=form.errors
            return HttpResponse(msg)


"""
    container page in job
"""
class ContainerView(LoginRequiredMixin, View):
    login_url               = 'login'
    template_name           = 'wenjian/container.html'
    form_class              = ContainerForm

    # Views for initiate
    def get(self, request, *args, **kwargs):

        if 'job_no' in self.kwargs:             # New Container
            form            = self.form_class(None)
            pk              = self.kwargs['job_no']
            job_no          = job.objects.get(id=pk).job_no
            print("new")

        else:                                   # Update Container
            if 'pk' in self.kwargs:
#                pk              = self.kwargs['pk']
                init_form       = container.objects.get(pk=self.kwargs['pk'])
                job_no          = init_form.job_no
                pk              = init_form.job_no_id

                form            = self.form_class(instance = init_form)       
        return render(request, self.template_name, {'form': form, "job_no": job_no, 'pk': pk,})
    

    # Save data from views
    def post(self, request, *args, **kwargs):
        form                            = self.form_class(request.POST)

        if form.is_valid():
            if 'job_no' in self.kwargs:             # New Container Insert
                pk                          = self.kwargs['job_no']
                job_no                      = job.objects.get(id=pk).job_no
                new_container           = container(
                    job_no_id           = int(pk),
                    containerno         = form.cleaned_data['containerno'],
                    containersize       = form.cleaned_data['containersize'],
                    sealno              = form.cleaned_data['sealno'],
                    weight              = form.cleaned_data['weight'],
                    volume              = form.cleaned_data['volume'],
                    packages            = form.cleaned_data['packages'],
                    amount_of_package   = form.cleaned_data['amount_of_package'],   
                    update_date         = datetime.date.today(),                  
                )

                new_container.save()
            else:                                   # Old Container Update
                update_container            = container.objects.get(pk=self.kwargs['pk'])
                job_no                      = update_container.job_no
                pk                          = update_container.job_no_id

                update_container.containerno            = form.cleaned_data['containerno']
                update_container.containersize          = form.cleaned_data['containersize']
                update_container.sealno                 = form.cleaned_data['sealno']
                update_container.weight                 = form.cleaned_data['weight']
                update_container.volume                 = form.cleaned_data['volume']
                update_container.packages               = form.cleaned_data['packages']
                update_container.amount_of_package      = form.cleaned_data['amount_of_package']   
                update_container.update_date            = datetime.date.today() 

                update_container.save()
        else:
            print(form.errors)
            return HttpResponse('wrong')
        return HttpResponseRedirect(reverse('containerlist', args=[pk]))


        

class CntrListView(LoginRequiredMixin, View):
    login_url = 'login'

    template_name           = 'wenjian/containerlist.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['job_no']
        job_no = job.objects.get(id=pk).job_no
        table_list = container.objects.filter(job_no_id = pk)
        return render(request, self.template_name, {'table_list':table_list, 'pk': pk, 'job_no': job_no,})

#        return HttpResponse(msg)

"""Use class-FormView to create a simple View for a Form"""
class PortNew(CreateView):
    model               = port
    form_class          = PortForm
    template_name       = 'wenjian/port.html'

class PortUpdate(UpdateView):
    model               = port
    template_name       = 'wenjian/port.html'
    form_class          = PortForm

"""Use class-ListView to create a list page of model. Simple and efficient"""
class PortList(LoginRequiredMixin, ListView):
    login_url = 'login'

    model               = port
    context_object_name = 'port_list'
    template_name       = 'wenjian/portlist.html'
    queryset            = port.objects.order_by('port')


"""Currency View List == New/Update/List """
class CurrencyNew(CreateView):
    model               = currency
    template_name       = 'wenjian/currency.html'
    form_class          = CurrencyForm

class CurrencyUpdate(UpdateView):   
    model               = currency
    form_class          = CurrencyForm
    template_name       = 'wenjian/currency.html'

class CurrencyList(ListView):
    model               = currency
    template_name       = 'wenjian/currencylist.html'
    context_object_name = 'currency_list'
    queryset            = currency.objects.all().order_by('-updatedate')

"""ROLE views"""
class RoleNew(CreateView):
    model               = role
    form_class          = RoleForm
    template_name       = 'wenjian/role.html'

class RoleUpdate(UpdateView):   
    model               = role
    form_class          = RoleForm
    template_name       = 'wenjian/role.html'

class RoleList(ListView):
    model               = role
    template_name       = 'wenjian/rolelist.html'
    context_object_name = 'role_list'
    queryset            = role.objects.all().order_by('role')
"""--------"""

"""Expense views"""
class ExpenseNew(CreateView):
    model               = expense
    form_class          = ExpenseForm
    template_name       = 'wenjian/expense.html'

class ExpenseUpdate(UpdateView):   
    model               = expense
    form_class          = ExpenseForm
    template_name       = 'wenjian/expense.html'

class ExpenseList(ListView):
    model               = expense
    template_name       = 'wenjian/expenselist.html'
    context_object_name = 'expense_list'
    queryset            = expense.objects.all().order_by('expense')
"""--------"""

"""Containersize views"""
class ContainersizeNew(CreateView):
    model               = containersize
    form_class          = ContainersizeForm
    template_name       = 'wenjian/containersize.html'

class ContainersizeUpdate(UpdateView):   
    model               = containersize
    form_class          = ContainersizeForm
    template_name       = 'wenjian/containersize.html'

class ContainersizeList(ListView):
    model               = containersize
    template_name       = 'wenjian/containersizelist.html'
    context_object_name = 'containersize_list'
    queryset            = containersize.objects.all().order_by('containersize')
"""--------"""


"""USER views"""
class UserList(ListView):
    model               = branch_user
    template_name       = 'wenjian/userlist.html'
    context_object_name = 'user_list'
    queryset            = branch_user.objects.all().order_by('username')

class User(View):
    form_class          = UserForm
    template_name       = 'wenjian/user.html'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid:
            user = form.save(commit = False)
            username            = form.cleaned_data['username']
            password            = form.cleaned_data['password']
            first_name          = form.cleaned_data['first_name']
            last_name           = form.cleaned_data['last_name']
            validate_date       = form.cleaned_data['validate_date']

            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse('userlist'))
        return HttpResponse("post")

class UpdateUser(UpdateView):
    model               = branch_user
    template_name       = 'wenjian/user.html'
    form_class          = UserUpdateForm



"""
    This is for password change
    The password could not be shown as string. 
    in this system, only administrator can change password for all user.
"""
class ChangePassword(View):
    template_name = 'wenjian/password.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        
        new_pwd_1 = self.request.POST.get('new_password_1')
        new_pwd_2 = self.request.POST.get('new_password_2')

        if new_pwd_1 == new_pwd_2:
            checkstr   = True
            if len(new_pwd_1) < 6:
                msg = "The password is too short than 6 digits!"
                checkstr = False
            else:
                for i in new_pwd_1:
                    if i.isspace():
                        checkstr = False
                        msg = "There should be no space in Password!"
        else:
            checkstr = False
            msg = "Two new passwords are not same!"
        
        if checkstr:
            user = User.objects.get(id=pk)
            user.set_password(new_pwd_1)
            user.save()
            return HttpResponseRedirect(reverse('userlist'))
        else:
            return render(request, self.template_name, {'msg':msg})



"""Some functions used in this file"""
def select_client(client_id):
        select_client = client.objects.get(id=client_id)
        select_client = select_client.client_shortcut

        return select_client