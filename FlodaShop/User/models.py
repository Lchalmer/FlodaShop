# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from FlodaShop import model_sharding


class User(models.Model):
    snowID = models.BigIntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=20)
    is_active = models.IntegerField(default=0)
    is_delete = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    station = models.IntegerField(default=1,
                                  choices=[(0, 'admin'),
                                           (1, 'staff'),
                                           (2, 'leader'),
                                           (3, 'boss')])

    class Meta:
        # abstract = True
        db_table = 'user'

    def __str__(self):
        return self.username

