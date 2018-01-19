from django.contrib import admin

# Register your models here.
from wenjian.models import client_pic
from wenjian.models import client, client_role

admin.site.register(client_pic)
admin.site.register(client)
admin.site.register(client_role)