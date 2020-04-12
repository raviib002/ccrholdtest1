from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from audit_log.models.fields import CreatingUserField, LastUserField
from django.db.models.deletion import CASCADE
from random import choices
# Create your models here.

#Creating model for Status Table Starts here
class Status(models.Model):
    STATUS_CHOICES = (
        (u'0', u'InActive'),
        (u'1', u'Active'),
    )
    status_name = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name=_("Status"))
    created_by = CreatingUserField(related_name = "StatusCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "StatusUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.status_name
    
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"
        db_table = 'ccrh_master_status'
        
#Creating model for state Table Starts here
class State(models.Model):
    state_name = models.CharField(max_length=100, verbose_name=_("State Name"))
    country_id = models.IntegerField(default=1,verbose_name=_("Country Id"))
    status =  models.ForeignKey(Status,  on_delete=models.CASCADE, verbose_name=_("Status Id"))
    created_by = CreatingUserField(related_name = "StateCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "StateUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.state_name
    
    class Meta:
        verbose_name = "State"
        verbose_name_plural = "State"
        db_table = 'ccrh_master_state'
#Creating model for city Table Starts here
class City(models.Model):
    city_name = models.CharField(max_length=100, verbose_name=_("State Name"))
    state =  models.ForeignKey(State,  on_delete=models.CASCADE, verbose_name=_("State Id"))
    status =  models.ForeignKey(Status,  on_delete=models.CASCADE, verbose_name=_("Status Id"))
    created_by = CreatingUserField(related_name = "CityCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "CityUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.city_name
    
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "City"
        db_table = 'ccrh_master_city'
        
        