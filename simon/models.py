import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class payee(models.Model):
    payee = models.CharField(max_length=150)

    def __str__(self):
        return self.payee

class paytype(models.Model):
    pay_type = models.CharField(max_length=50)
    
    def __str__(self):
        return self.pay_type
    
class pay(models.Model):
    payee           = models.ForeignKey(payee, on_delete=models.CASCADE)
    pay_amount      = models.DecimalField(max_digits = 6, decimal_places = 2)
    pay_date        = models.DateField(auto_now = False, auto_now_add=False)
    start_date      = models.DateField(auto_now=False, auto_now_add=False, default=datetime.date.today)
    end_date        = models.DateField(auto_now=False, auto_now_add=False, default=datetime.date.today)
    payment_type    = models.ForeignKey(paytype, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.payee)