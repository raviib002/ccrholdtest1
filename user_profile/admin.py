"""
Project    : "CCRH"
module     : User Profile/admin
created    : 03/03/2020
Author     : Manish Kumar
"""

from django.contrib import admin
from user_profile.models import (
                           Profilestatus,
                           )

# Register your models here.
class ProfilestatusAdmin(admin.ModelAdmin):
    list_display = ('profile_status',)
    

    
admin.site.register(Profilestatus, NewsAdmin)
