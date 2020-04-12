from django.db import models
from django.utils.translation import ugettext_lazy as _
from audit_log.models.fields import CreatingUserField, LastUserField
from django.contrib.auth.models import User, Group
from django.db.models.deletion import CASCADE
from random import choices
from master.models import (State,City)


#Creating model for Status Table Starts here
class Profilestatus(models.Model):
#     PROFILE_CHOICES = (
#         (u'1', u'Pending for Approval'),
#         (u'2', u'Approved'),
#         (u'3', u'Rejected'),
#         (u'4', u'Disabled'),
# 
#     )
    profile_status = models.CharField(max_length=50, verbose_name=_("Profile Status"))
    created_by = CreatingUserField(related_name = "ProfilestatusCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "ProfilestatusUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.status_name
    
    class Meta:
        verbose_name = "Profile status"
        verbose_name_plural = "Profile status"
        db_table = 'ccrh_user_profile_status'
        
#Default keeping the profile status 1
def get_profile_status():
    return Profilestatus.objects.get(profile_status="Pending for Approval")
        
#Creating model for Additional Profile Table Starts here
class AdditionalProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User Id"))
    mobile_no = models.BigIntegerField( verbose_name=_("Mobile Number "))
    addt_mobile_no = models.BigIntegerField(blank=True, null=True, verbose_name=_("Additional Mobile Number "))
    photo = models.ImageField(upload_to='Profile_image/', default='', blank=True, null=True, verbose_name="Profile Photo")
    address_line1 = models.TextField(blank=True, null=True,verbose_name=_("Address Line1")) 
    address_line2 = models.TextField(blank=True, null=True,verbose_name=_("Address Line2"))
    state =  models.ForeignKey(State, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("State Id"))
    city =  models.ForeignKey(City,  blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("City Id"))
    pincode = models.BigIntegerField(blank=True, null=True,  verbose_name=_("Pincode"))
    profile_status = models.ForeignKey(Profilestatus, default=get_profile_status,on_delete=models.CASCADE, verbose_name=_(" Profile status"))
    profile_approved_by =  models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Profile Approved By"), related_name = "ProfileApprovedBy")
    profile_approved_datetime = models.DateTimeField(verbose_name=(" Profile Approved Date Time"), blank=True, null=True)
    profile_approved_remarks = models.TextField(blank=True, null=True,verbose_name=_("Profile Approved Remarks")) 
    profile_dis_opt_by_remarks =  models.TextField(blank=True, null=True,verbose_name=_("Profile Dis Opt By Remarks")) 
    profile_dis_opt_by_datetime = models.DateTimeField(verbose_name=(" Profile Dis Opt By Datetime"), blank=True, null=True)
    profile_dis_by= models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Profile Dis By"), related_name = "ProfiledisBy")
    profile_dis_by_remarks = models.TextField(blank=True, null=True,verbose_name=_("Profile Disease By Remarks")) 
    profile_dis_by_datetime =  models.DateTimeField(verbose_name=(" Profile Dis By Datetime"), blank=True, null=True)
    created_by = CreatingUserField(related_name = "AdditionalProfileCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "AdditionalProfileUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    
    class Meta:
        verbose_name = "AdditionalProfile"
        verbose_name_plural = "AdditionalProfile"
        db_table = 'ccrh_user_additional_profile'