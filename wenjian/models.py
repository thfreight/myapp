from django.db import models
from django.urls import reverse
import datetime

from django.contrib.auth.models import Group, User

# Create your models here.

class branch_office(models.Model):
    office_shortcut     = models.CharField( max_length = 50,        verbose_name = "OFFICE SHORTCUT")
    office_name         = models.CharField( max_length = 150,       verbose_name = 'OFFICE NAME', )
    office_address      = models.TextField( max_length = 400,       verbose_name = 'OFFICE ADDRESS',)
    office_ac_code      = models.CharField( max_length = 5,         verbose_name = 'A/C CODE',)
    office_tel          = models.CharField( max_length = 20,        verbose_name = 'OFFICE TELEPHONE',)
    office_code         = models.CharField( max_length = 2,         verbose_name = "OFFICE CODE")
    update_date         = models.DateField(
        auto_now_add    = False,
        auto_now        = False,
        verbose_name    = "UPDATE-DATE",
        blank           = True,
    )
    def __str__(self):
        return self.office_shortcut

    def get_absolute_url(self):
        return reverse('officelist')

class branch_user(User):
    branch_office       = models.ForeignKey(
        'branch_office', 
        on_delete       = models.CASCADE,
        verbose_name    = "BRANCH OFFICE",
    )
    validate_date       = models.DateField(
        auto_now_add    = False,
        auto_now        = False,
        verbose_name    = "VALIDATE TO",
    )

    def __str__(self):
        return str(self.username)

    def get_absolute_url(self):
        return reverse('userlist')

class client(models.Model):
    client_shortcut     = models.CharField(max_length = 30)
    client_name         = models.CharField(max_length = 100)
    client_address      = models.TextField(max_length = 400)
    client_tel          = models.CharField(max_length = 30)
    client_email        = models.EmailField()
    update_date         = models.DateField(
        auto_now_add    = True,
        verbose_name    = "UPDATE DATE",
    )

    def __str__(self):
        return self.client_shortcut

class client_pic(models.Model):
    client              = models.ForeignKey(
        'client', 
        on_delete       = models.CASCADE,
        verbose_name    = 'CLIENT',
    )
    pic_name            = models.CharField(
        max_length=25,
        verbose_name    = "NAME",
    )
    pic_mobile          = models.CharField(
        max_length      = 25,
        verbose_name    = 'MOBILE',
    )
    pic_email           = models.EmailField(
        verbose_name    = 'E-MAIL',
    )
    pic_position        = models.CharField(
        max_length      = 10,
        verbose_name    = 'POSITION',
    )
    update_date         = models.DateField(
        auto_now_add    = True,
        verbose_name    = 'UPDATE DATE',
    )

    def __str__(self):
        return self.pic_name

    def get_absolute_url(self):
        return reverse('contactlist/<client_id>')

class currency(models.Model):
    currency            = models.CharField(
        max_length      = 8, 
        verbose_name    = "CURRENCY",
    )
    exchangerate        = models.DecimalField(
        max_digits      = 4, 
        decimal_places  = 2, 
        verbose_name    = 'EXCHANGE RATE',
    )
    updatedate          = models.DateField(
        auto_now_add    = False,
        auto_now        = False,
        verbose_name    = "UPDATE DATE",
    )
    startdate           = models.DateField(
        auto_now_add    = False,
        auto_now        = False,
        verbose_name    = "START DATE",
    )
    enddate             = models.DateField(
        auto_now_add    = False,
        auto_now        = False,
        verbose_name    = "END DATE",
    )
    update_date         = models.DateField(
        auto_now_add    = False,
        auto_now        = False,
        verbose_name    = "UPDATE-DATE",
        blank           = True,
    )
    def __str__(self):
        return self.currency
    
    
    def get_absolute_url(self):
        return reverse('currencylist')

class port(models.Model):
    port = models.CharField(max_length=50)
    update_date         = models.DateField(
        auto_now_add    = False,
        auto_now        = False,
        verbose_name    = "UPDATE DATE",
        blank           = True,
    )

    def __str__(self):
        return self.port

    def get_absolute_url(self):
        return reverse('portlist')


class job(models.Model):
    status_choice       = (
        ('NORMAL', 'NORMAL'),
        ('FINISHED', 'FINISHED'),
        ('VOIDED', 'VOIDED'),
    )

    job_no              = models.CharField(
        max_length      = 20, 
        verbose_name    = "JOB NO",
        blank           = True
    )
    booking_no          = models.CharField(
        max_length      = 20, 
        verbose_name    = "BOOKING NO", 
        blank           = True,
        null            = True,
    )
    client              = models.ForeignKey(
        'client', 
        on_delete       = models.CASCADE,
        verbose_name    = "CLIENT",
    )
    pol                 = models.ForeignKey(
        'port', 
        on_delete       = models.CASCADE, 
        verbose_name    = "PORT OF LOADING",
        related_name    ='loading',
    )
    pod                 = models.ForeignKey(
        'port', 
        on_delete       = models.CASCADE, 
        verbose_name    = "PORT OF DISCHARGING",
        related_name ='discharge',
    )
    vessel              = models.CharField(
        max_length      = 50, 
        verbose_name    = "VESSEL", 
        blank           = True,
        null            = True,
    )
    pre_carriage        = models.CharField(
        max_length      = 50, 
        verbose_name    = 'PRE-CARRIAGE', 
        blank           = True,
        null            = True,
    )
    doc                 = models.DateField(
        auto_now_add    = False, 
        auto_now        = False, 
        verbose_name    = "CLOSING DATE",
        blank           = True,
        null            = True,
    )
    etd                 = models.DateField(
        auto_now_add    = False, 
        auto_now        = False,
        verbose_name    = 'ESTIMATE DEPARTURE',
        blank           = True,
        null            = True,
    )
    eta                 = models.DateField(
        auto_now_add    = False, 
        auto_now        = False,
        verbose_name    = "ESTIMATE ARRIVAL",
        blank           = True,
        null            = True,
    )
    voyage              = models.CharField(
        max_length      = 50, 
        verbose_name    = "VOYAGE",
        blank           = True,
        null            = True,
    )
    book_agent          = models.ForeignKey(
        'client', 
        on_delete       = models.CASCADE, 
        verbose_name    = 'BOOKING AGENT', 
        related_name    = 'bookingagent',
        blank           = True,
        null            = True,
    )
    carrier             = models.ForeignKey(
        'client', 
        on_delete       = models.CASCADE, 
        verbose_name    = 'CARRIER', 
        related_name    = "shippingline",
        blank           = True,
        null            = True,
    )
    destination_agent   = models.ForeignKey(
        'client', 
        on_delete       = models.CASCADE, 
        verbose_name    = "RELEASE AGENT", 
        related_name    = "releaseagent",
        blank           = True,
        null            = True,
    )
    create_date         = models.DateField(
        auto_now_add    = False, 
        auto_now        = False,
        verbose_name    = 'DATE OF CREATE',
        blank           = True,
    )
    finish_date         = models.DateField(
        auto_now_add    = False, 
        auto_now        = False,
        verbose_name    = "FINISH DATE",
        blank           = True,
        null            = True,
    )
    status              = models.CharField(
        max_length      = 20,
        choices         = status_choice, 
        verbose_name    = 'JOB STATUS',
    )
    place_of_receipt    = models.CharField(
        max_length      = 30, 
        verbose_name    = "PLACE OF RECEIPT",
        blank           = True,
        null            = True,
    )
    place_of_delivery   = models.CharField(
        max_length      = 30, 
        verbose_name    = "PLACE OF DELIVERY",
        blank           = True,
        null            = True,
    )
    operator            = models.ForeignKey(
        branch_user,
        on_delete       = models.CASCADE,
        verbose_name    = 'OPERATOR',
        related_name    = "operator",
    )
    assistant           = models.ForeignKey(
        branch_user,
        on_delete       = models.CASCADE,
        verbose_name    = 'ASSISTANT',
        blank           = True,
        related_name    = "assistant",
        null            = True,
    )
    creator             = models.ForeignKey(
        branch_user,
        on_delete       = models.CASCADE,
        verbose_name    = 'CREATOR',
        blank           = True,
        related_name    = "creator",
    )
    update_date         = models.DateField(
        auto_now_add    = True,
        verbose_name    = 'UPDATE DATE',
    )

    def __str__(self):
        return self.job_no

class containersize(models.Model):
    containersize       = models.CharField(
        max_length      = 8,
        verbose_name    = "CNTR SIZE",
    )
    update_date         = models.DateField(
        auto_now_add    = True,
        verbose_name    = 'UPDATE DATE',
    )

    def __str__(self):
        return self.containersize

    def get_absolute_url(self):
        return reverse('containersizelist')

class container(models.Model):
    job_no              = models.ForeignKey(
        'job', 
        on_delete       = models.CASCADE,
        verbose_name    = 'JOB NO',
        blank           = True,
    )
    containerno         = models.CharField(
        max_length      = 14, 
        verbose_name    = "CONTAINER NO",
        blank           = True,
        null            = True,
    )
    containersize       = models.ForeignKey(
        'containersize', 
        on_delete       = models.CASCADE, 
        verbose_name    = 'CONTAINER SIZE',
        blank           = True,
        null            = True,
    )
    sealno              = models.CharField(
        max_length      = 20, 
        verbose_name    = 'SEAL NO.', 
        blank           = True,
        null            = True,
    )
    weight              = models.DecimalField(
        max_digits      = 10, 
        decimal_places  = 4, 
        verbose_name    = 'WEIGHT',
        blank           = True,
        null            = True,
    )
    volume              = models.DecimalField(
        max_digits      = 10, 
        decimal_places  = 4, 
        verbose_name    = 'VOLUME',
        blank           = True,
        null            = True,
    )
    packages            = models.ForeignKey(
        'package', 
        on_delete       = models.CASCADE,
        verbose_name    = 'PACKAGE',
        blank           = True,
        null            = True,
    )
    amount_of_package   = models.PositiveIntegerField(
        verbose_name    = 'AMOUNT',
        blank           = True,
        null            = True,
    )
    update_date         = models.DateField(
        verbose_name    = 'UPDATE DATE',
        blank           = True,
    )

    def __str__(self):
        if self.containerno:
            return self.containerno
        else:
            return "Container"

class package(models.Model):
    package             = models.CharField(
        max_length      = 20, 
        verbose_name    = "PACKAGE",
    )
    update_date         = models.DateField(
        auto_now_add    = True,
        verbose_name    = 'UPDATE DATE',
        blank           = True,
    )

    def __str__(self):
        return self.package

    def get_absolute_url(self):
        return reverse('packagelist')

class commodity(models.Model):
    job_no              = models.ForeignKey(
        'job', 
        on_delete       = models.CASCADE,
        verbose_name    = "JOB NO",
    )
    commodity           = models.TextField(
        max_length      = 800, 
        verbose_name    = "GOOD DESCRIPTION",
        blank           = False,
    )
    shipping_mark       = models.TextField(
        max_length      =800, 
        verbose_name    = "SHIPPING MARK",
    )
    update_date         = models.DateField(
        auto_now_add    = True,
        verbose_name    = 'UPDATE DATE',
        blank           = True,
    )


    def __str__(self):
        return str(self.job_no)

class role(models.Model):
    role                = models.CharField(
        max_length      = 30,
        verbose_name    = "ROLE",
    )
    update_date         = models.DateField(
        auto_now_add    = True,
        verbose_name    = 'UPDATE DATE',
        blank           = True,
    )


    def __str__(self):
        return self.role

    def get_absolute_url(self):
        return reverse('rolelist')


"""Each client has own role either single or multi"""
class client_role(models.Model):
    client              = models.ForeignKey(
        'client', 
        on_delete       = models.CASCADE,
        verbose_name    = "CLIENT",
    )
    role                = models.ForeignKey(
        'role', 
        on_delete       = models.CASCADE,
        verbose_name    = "ROLE",
    )
    update_date         = models.DateField(
        auto_now_add    = True,
        verbose_name    = 'UPDATE DATE',
        blank           = True,
    )

    def __str__(self):
        return str(self.client)


class expense(models.Model):
    expense             = models.CharField(
        max_length      = 30,
        verbose_name    = "EXPENSE",
    )
    update_date         = models.DateField(
        auto_now_add    = True,
        verbose_name    = 'UPDATE DATE',
        blank           = True,
    )

    def __str__(self):
        return self.expense

    def get_absolute_url(self):
        return reverse('expenselist')