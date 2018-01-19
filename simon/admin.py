from django.contrib import admin

# Register your models here.
from .models import payee
from .models import paytype
from .models import pay

admin.site.register(payee)
admin.site.register(paytype)
admin.site.register(pay)