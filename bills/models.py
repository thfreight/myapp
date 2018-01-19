from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

class photo(models.Model):
    photo = models.ImageField(height_field=1000, width_field=1000)
    upload = models.FileField()

class simon(models.Model):
    update_date = models.DateField(
        auto_now_add = True,
#        auto_now    = True,
    )
    name = models.CharField(max_length = 10)

    def __str__(self):
        return self.name


class backup_record(models.Model):
    tablename = models.CharField(max_length = 100)
    last_backup_date = models.DateField(auto_now_add=False, auto_now=False)
    backup_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.tablename