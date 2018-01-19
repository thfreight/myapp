from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import datetime
from datetime import timedelta

# Import my own models/Database
from .models import payee, paytype, pay
import simon.models

# Import Forms.
from .forms import NameForm, payeeForm, expenseForm, paymentForm

#import my private classes
from simon.myclass import monthinyear
from simon.myclass import month_record

def index(request):
    last_payment = pay.objects.order_by('-pay_date')[:12]
    for e in last_payment:
        e.pay_date      = my_date_format(e.pay_date)
        e.start_date    = my_date_format(e.start_date)
        e.end_date      = my_date_format(e.end_date)

    return render(request, 'simon/index.html', {'last_payment': last_payment})

def payeelist(request):
    payee_list  = payee.objects.all().order_by('payee')
    return render(request, 'simon/payee.html', {'payee_list' : payee_list})

# New Payee, Modify Payee, response to url: /payee/[int] int=0: New, int>0: modify
def payeedetail(request, payee_id):
    if payee_id == '0':
        form        = payeeForm()
    else:
        this_payee  = get_object_or_404(payee, pk=payee_id)
        payee_id    = this_payee.id
        form        = payeeForm(initial={'payee': this_payee.payee})
    return render(request, 'simon/payeedetail.html', {'form' : form, 'payee_id': payee_id})

def savepayee(request, payee_id):
    if payee_id=='0':
        if request.POST['payee'] != "":
            new_payee       =payee(payee=request.POST['payee'].upper())
            new_payee.save()
    else:
        updated_payee       = get_object_or_404(payee, pk=payee_id)
        updated_payee.payee =request.POST['payee'].upper()
        updated_payee.save()
    return HttpResponseRedirect(reverse('payee'))

# Expenses Page
# Expense List
def expense(request):
    expense_list = paytype.objects.order_by('pay_type')
    return render(request, 'simon/expense.html', {'expense_list' : expense_list})

# Mofity, New Expense Type.
def expensedetail(request, expense_id):
    if request.method == "POST":
        form                            = expenseForm(request.POST)
        if form.is_valid():
            this_input_expense          = form.cleaned_data['expense'].upper()
            if expense_id == '0':
                expense_model           = paytype(pay_type = this_input_expense)
            else:
                expense_model           = get_object_or_404(paytype, pk = expense_id)
                expense_model.pay_type  = this_input_expense
            expense_model.save()
            return HttpResponseRedirect(reverse('expense'))
    else:
        if expense_id == '0':
            form                        = expenseForm()
        else: 
            this_expense                = get_object_or_404(paytype, pk=expense_id)
            expense_id                  = this_expense.id
            form                        = expenseForm(initial={'expense': this_expense.pay_type})
        return render(request, 'simon/expensedetail.html', { 'form' : form, 'expense_id': expense_id } )

def payment(request):
    if request.method == 'POST':
        form = paymentForm(request.POST)
        if form.is_valid():
            form.save()
    form = paymentForm()
    return render(request, 'simon/payment.html', {'form': form})

def chaxun(request, year_id):
    #set up the month sequence.
    enq_year = int(year_id)
    month_class = monthinyear(year_id)
    month_list = month_class.first_last_day()

    # Setup the year to show in the Nav   
    last_year = enq_year - 1
    next_year = enq_year + 1
    this_year = datetime.date.today().year

    month_record = []
    aCount = 0
    while aCount < 23:
        d=monthinyear.date_makeup(month_list[aCount])

        pay_record = pay.objects.filter(end_date__gte = month_list[aCount+1], start_date__lte = month_list[aCount])
        month_record.append(avr_pay_mount(pay_record, d))
        aCount = aCount + 2
    
    # Payee List as table head
    payee_head = []
    payee_head = payee.objects.values('id', 'payee').order_by('payee')
#    for p in payee_all:
#        payee_head.append(p['payee'])
#        payee_head.append(p['id'])

    return render(request, 'simon/chaxun.html', {   'month_record'  : month_record, 
                                                    'payee_head'    : payee_head,
                                                    'this_year'     : this_year,
                                                    'last_year'     : last_year,
                                                    'next_year'     : next_year,
                                                    'year_id'       : year_id,
                                                    })

# This function to calculate each payment for each payee
# If multi payment of same payee, add them together.
# If payment for several months, average them for each month.
def avr_pay_mount(pay_record, month_no):
    # Calculate average amount of more months payment. Restore into pay_record
    dAmount = 0
    for e in pay_record:
        dDate=e.end_date - e.start_date
        dDate = dDate.days
        dDate = int(dDate/30)
        if dDate > 1:
            dAmount = round(e.pay_amount/dDate, 2)
            e.pay_amount = dAmount

    # create array refill_month_list to store each payment for each payee
    # output formate: [year-month, 8888,8888,...., month_total]
    all_payee = payee.objects.all().order_by('payee')
    refill_month_list=[]
    refill_month_list.append(month_no)
    month_ttl_amount = 0
    for f in all_payee:
        ttl_amount = 0
        for e in pay_record:
            if e.payee.payee == f.payee:
                ttl_amount = ttl_amount + e.pay_amount
        refill_month_list.append(ttl_amount)
        month_ttl_amount = month_ttl_amount + ttl_amount
        
    refill_month_list.append(month_ttl_amount)

    return refill_month_list

def pmtdtl(request, payee_id, year_id):
    this_month      = monthinyear(year_id)
    month_day_list  = this_month.first_last_day()

    month_list = month_record(month_day_list[0], month_day_list[1], payee_id, 'pay')
    table_head = month_list.retrieve_head()

    varCount = 0
    table_content = []
    while varCount < 23:
        month_pay_content = []
        table_month = monthinyear.date_makeup(month_day_list[varCount])

        # Month Append
        month_pay_content.append(table_month)

        # Find monthly data
        this_record = pay.objects.filter(
                start_date__gte 	= month_day_list[varCount], 
                end_date__lte 	    = month_day_list[varCount+1], 
                payee 		        = payee_id,
                                        )  
        if this_record:
            pass
        else:
            last_record = pay.objects.filter(
                start_date__gte 	= month_day_list[varCount-2], 
                end_date__lte 	    = month_day_list[varCount-1], 
                payee 		        = payee_id,            
            )
#            next_record = pay.objects.filter(
#                start_date__gte 	= month_day_list[varCount+2], 
#                end_date__lte 	    = month_day_list[varCount+3], 
#                payee 		        = payee_id,            
#            )
            if last_record:
                pass
            else:
#                if next_record:
#                    pass
#                else:
                this_record = pay.objects.filter(
                pay_date__gte 	    = month_day_list[varCount], 
                pay_date__lte 	    = month_day_list[varCount+1], 
                payee 		        = payee_id,                
                )                

        ttl_month = 0
        var_payday = datetime.date.today()
        for h in table_head:
            this_item_amount = 0
            for c in this_record:
                if c.payment_type.pay_type == h:
                    this_item_amount = c.pay_amount
                    var_payday = c.pay_date
            ttl_month = ttl_month + this_item_amount
            month_pay_content.append(this_item_amount)

        l=len(month_pay_content)-1
        if ttl_month != 0:
            month_pay_content[l] = my_date_format(var_payday)
        else:
            month_pay_content[l] = ''

        month_pay_content.append(ttl_month)
        varCount +=2
        table_content.append(month_pay_content)

    var_payee = payee.objects.get(pk=payee_id)
    payee_id = var_payee.payee

    return render(request, 'simon/pmtdtl.html',{ 'table_head'       : table_head,
                                                 'table_content'    : table_content,
                                                 'year_id'          : year_id,
                                                 'payee_id'         : payee_id, 
                                                } )

def my_date_format(idate):
    iyear   = idate.year
    imonth  = idate.month
    iday    = idate.day

    if imonth < 10:
        imonth = '0'+str(imonth)
    else:
        imonth = str(imonth)
    if iday < 10:
        iday = '0'+str(iday)
    else:
        iday = str(iday)

    new_date_format = str(iyear)+'-'+imonth+'-'+iday
    return new_date_format