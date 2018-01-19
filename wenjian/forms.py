from django import forms
from django.contrib.auth.models import User, Group
import datetime

from wenjian.models import client, job, port, currency, client_role
from wenjian.models import client_pic, role, expense, containersize
from wenjian.models import branch_office, branch_user, container

"""Login Form """
class LoginForm(forms.Form):
    username = forms.CharField(label = 'USER NAME', widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label = 'PASSWORD' , widget = forms.PasswordInput(attrs={'class':'form-control'}))
    
"""------"""

class client_form(forms.ModelForm):

    class Meta:
        model       = client
        fields      = '__all__'
        labels      = {
            'client_shortcut'  : 'SHORT NAME',
            'client_name'      : 'FULL NAME',
            'client_address'   : 'ADDRESS',
            'client_tel'       : 'TELEPHONE',
            'client_email'     : 'E-MAIL',
        }
        widgets = {
            'client_shortcut'  : forms.TextInput(attrs={'class':'form-control',}),
            'client_name'      : forms.TextInput(attrs={'size': 30, 'class':'form-control',}),
            'client_address'   : forms.Textarea(attrs={'rows':5, 'cols':50, 'class':'form-control'}),
            'client_tel'       : forms.TextInput(attrs={'class':'form-control'}),
            'client_email'     : forms.EmailInput(attrs={'size' : 45, 'class':'form-control',}),
        }

class client_list_form(forms.Form):
    search_content = forms.CharField(
            max_length          = 10,
            widget              = forms.TextInput(attrs = {'class': 'form-control mr-sm-2'}),
        )

class contact_form(forms.ModelForm):

    class Meta:
        model                   = client_pic
        fields                  = ['pic_name', 'pic_mobile', 'pic_email']
        widgets                 = {
            'pic_name'          : forms.TextInput(attrs={'class':'form-control',}),
            'pic_mobile'        : forms.TextInput(attrs={'class':'form-control',}),
            'pic_email'         : forms.EmailInput(attrs={'class':'form-control',}),
        }
        labels                  = {
            'pic_name'          : ('PERSON NAME'),
            'pic_mobile'        : ('MOBILE PHONE'),
            'pic_email'         : ('E-Mail'),
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class job_form(forms.ModelForm):

    class Meta:
        model = job
        fields = ('__all__')
 
        widgets = {
            'etd'               : DateInput(attrs={'class': 'form-control',}),
            'eta'               : DateInput(attrs={'class': 'form-control',}),
            'pol'               : forms.Select(choices = (port.objects.order_by('port'),),attrs={'class': 'form-control',}),
            'pod'               : forms.Select(choices = (port.objects.order_by('port'),),attrs={'class': 'form-control',}),
            'job_no'            : forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly',}),
            'booking_no'        : forms.TextInput(attrs={'class':'form-control',}),
            'client'            : forms.Select(attrs={'class':'form-control',}),
            'book_agent'        : forms.Select(attrs={'class':'form-control',}),
            'carrier'           : forms.Select(attrs={'class':'form-control',}),      
            'destination_agent' : forms.Select(attrs={'class':'form-control',}),       
            'create_date'       : forms.DateInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'finish_date'       : forms.DateInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'doc'               : DateInput(attrs={'class': 'form-control',}),
            'status'            : forms.Select(attrs={'class': 'form-control'}),
            'pre_carriage'      : forms.TextInput(attrs={'class': 'form-control',}),
            'vessel'            : forms.TextInput(attrs={'class': 'form-control',}),
            'voyage'            : forms.TextInput(attrs={'class': 'form-control',}),
            'place_of_receipt'  : forms.TextInput(attrs={'class': 'form-control',}),
            'place_of_delivery' : forms.TextInput(attrs={'class': 'form-control',}),      
            'operator'          : forms.Select(attrs={'class': 'form-control'}),
            'assistant'         : forms.Select(attrs={'class': 'form-control'}),
        }


class ContainerForm(forms.ModelForm):

    class Meta:
        model                   = container
        fields                  = ('__all__')
        widgets                 = {
            'containerno'       : forms.TextInput(attrs={'class':'form-control',}),
            'containersize'     : forms.Select(attrs={'class':'form-control',}),
            'sealno'            : forms.TextInput(attrs={'class':'form-control',}),
            'weight'            : forms.NumberInput(attrs={'class':'form-control',}),
            'volume'            : forms.NumberInput(attrs={'class':'form-control',}),
            'packages'          : forms.Select(attrs={'class':'form-control',}),
            'amount_of_package' : forms.NumberInput(attrs={'class':'form-control',}), 
        }       


class PortForm(forms.ModelForm):

    class Meta:
        model               = port
        fields              = ('__all__')
        widgets             = {
            'port'  : forms.TextInput(attrs={'class':'form-control',}),
        }
        labels              = {
            'port'          : ('PORT'),
        }

class CurrencyForm(forms.ModelForm):

    class Meta:
        model               = currency
        fields              = ('__all__')
        widgets             = {
            'currency'      : forms.TextInput(attrs={'class':'form-control',}),
            'exchangerate'  : forms.NumberInput(attrs={'class':'form-control',}),
            'startdate'     : DateInput(attrs={'class':'form-control',}),
            'enddate'       : DateInput(attrs={'class':'form-control',}),
        }
        labels              = {
            'startdate'     : ('START DATE'),
            'enddate'       : ('END DATE'),
            'currency'      : ('CURRENCY'),
            'exchangerate'  : ('EXCHANGE RATE'),
        }

class RoleForm(forms.ModelForm):

    class Meta:
        model               = role
        fields              = ('__all__')
        widgets             = {
            'role'          : forms.TextInput(attrs={'class':'form-control',}),
        }
        labels              = {
            'role'          : ('ROLE'),
        }


class ExpenseForm(forms.ModelForm):

    class Meta:
        model               = expense
        fields              = ('__all__')
        widgets             = {
            'expense'       : forms.TextInput(attrs={'class':'form-control',}),
        }
        labels              = {
            'expense'          : ('EXPENSE'),
        }

class ContainersizeForm(forms.ModelForm):

    class Meta:
        model               = containersize
        fields              = ('__all__')
        widgets             = {
            'containersize' : forms.TextInput(attrs={'class':'form-control',}),
        }
        labels              = {
            'containersize' : ('CONTAINER SIZE'),
        }

class OfficeForm(forms.ModelForm):

    class Meta:
        model                   = branch_office
        fields                  = ('__all__')
        widgets                 = {
            'office_name'       : forms.TextInput(attrs={'class':'form-control',}),
            'office_code'       : forms.TextInput(attrs={'class':'form-control',}),
            'office_ac_code'    : forms.TextInput(attrs={'class':'form-control',}),
            'office_tel'        : forms.TextInput(attrs={'class':'form-control',}),
            'office_shortcut'   : forms.TextInput(attrs={'class':'form-control',}),
            'office_address'    : forms.Textarea(attrs={'rows':5, 'cols':50, 'class':'form-control',}),
        }


class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model                   = branch_user
        fields                  = [
            'username',
            'first_name',
            'last_name',
            'email',
            'branch_office',
            'validate_date',
        ]
        widgets                 = {
            'username'          : forms.TextInput(attrs={'class':'form-control',}),
            'first_name'        : forms.TextInput(attrs={'class':'form-control',}),
            'last_name'         : forms.TextInput(attrs={'class':'form-control',}),
            'email'             : forms.EmailInput(attrs={'class':'form-control',}),
            'branch_office'     : forms.Select(attrs={'class':'form-control',}),
            'validate_date'     : DateInput(attrs={'class':'form-control',}),
        }
        labels                  = {
            'username'          : ("USER NAME"),
            'first_name'        : ('FIRST NAME'),
            'last_name'         : ('LAST NAME'),
            'email'             : ('EMAIL ADDRESS'),            
        }

class UserForm(forms.ModelForm):
    password                    = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control',}))

    class Meta:
        model                   = branch_user
        fields                  = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'branch_office',
            'validate_date',
        ]
        widgets                 = {
            'username'          : forms.TextInput(attrs={'class':'form-control',}),
            'password'          : forms.PasswordInput(attrs={'class':'form-control',}),
            'first_name'        : forms.TextInput(attrs={'class':'form-control',}),
            'last_name'         : forms.TextInput(attrs={'class':'form-control',}),
            'email'             : forms.EmailInput(attrs={'class':'form-control',}),
            'branch_office'     : forms.Select(attrs={'class':'form-control',}),
            'validate_date'     : DateInput(attrs={'class':'form-control',}),
        }
        labels                  = {
            'username'          : ("USER NAME"),
            'password'          : ('PASSWORD'),
            'first_name'        : ('FIRST NAME'),
            'last_name'         : ('LAST NAME'),
            'email'             : ('EMAIL ADDRESS'),            
        }