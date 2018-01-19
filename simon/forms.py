from django import forms
from .models import payee, pay

class NameForm(forms.Form):
    your_name   = forms.CharField(max_length = 100)
    your_mai    = forms.EmailField()
    message     = forms.CharField(widget = forms.Textarea)

# Payee Forms
class payeeForm(forms.Form):
    payee       = forms.CharField(widget = forms.TextInput())

class expenseForm(forms.Form):
    expense     = forms.CharField(widget = forms.TextInput())

class DateInput(forms.DateInput):
    input_type = 'date'

class paymentForm(forms.ModelForm):

    class Meta:
        model = pay
        fields = [  'payee', 
                    'pay_amount', 
                    'pay_date', 
                    'start_date',
                    'end_date',
                    'payment_type',]
        widgets = {
            'start_date'    : DateInput(),
            'pay_date'      : DateInput(),
            'end_date'      : DateInput(),
        }