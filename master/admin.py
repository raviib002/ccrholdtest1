"""
Project    : "CCRH"
module     : master/admin
created    : 03/03/2020
Author     : Manish Kumar
"""

from django.contrib import admin
from master.models import (News,
                           Downloads,
                           QuickLink,
                           Media,
                           State,
                           City,
                            Status,
                           )
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, DateTimeWidget, IntegerWidget
from import_export.admin import ImportMixin, ExportMixin, ImportExportMixin
from import_export.formats import base_formats
from django.forms import forms, ModelForm, Select
from django.contrib import admin
from import_export import resources, fields
# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_headline', 'desc')
    search_fields = ('news_headline',)
    
class DownloadsAdmin(admin.ModelAdmin):
    list_display = ('download_headline', 'desc')
    search_fields = ('download_headline',)
    
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ('headline', 'link')
    search_fields = ('headline',)
    
class MediaAdmin(admin.ModelAdmin):
    list_display = ('headline', )
    search_fields = ('headline',)

#status admin starts here    
class StatusResource(resources.ModelResource):
    status_name = fields.Field(column_name='Status name', attribute='status_name')
    
    class Meta:
        model = Status
        fields = ('status_name', )
        import_id_fields = fields
        export_order = fields
    
class StatusAdmin(ImportExportModelAdmin):
    resource_class = StatusResource
    list_display = ('status_name', )
    search_fields = ('status_name',)
    
class StateResource(resources.ModelResource):
    state_name = fields.Field(column_name='State name', attribute='state_name')
    country_id = fields.Field(column_name='Country Id', attribute='country_id',)
    status = fields.Field(column_name='Status', attribute='status', widget=ForeignKeyWidget(Status, 'status_name'))
    
    
    class Meta:
        model = State
        fields = ('state_name','country_id','status', )
        import_id_fields = fields
        export_order = fields
    
class StateAdmin(ImportExportModelAdmin):
    resource_class = StateResource
    list_display = ('state_name','country_id','status', )
    search_fields = ('state_name','')
    
    
class CityResource(resources.ModelResource):
    city_name = fields.Field(column_name='City name', attribute='city_name')
    state = fields.Field(column_name='State', attribute='state', widget=ForeignKeyWidget(State, 'state_name'))
    status = fields.Field(column_name='Status', attribute='status', widget=ForeignKeyWidget(Status, 'status_name'))
    
    
    class Meta:
        model = City
        fields = ('city_name', 'state', 'status')
        import_id_fields = fields
        export_order = fields
    
    
class CityAdmin(ImportExportModelAdmin):
    resource_class = CityResource
    list_display = ('city_name','state','status', )
    search_fields = ('city_name',)
    
admin.site.register(News, NewsAdmin)
admin.site.register(Downloads, DownloadsAdmin)
admin.site.register(QuickLink, QuickLinkAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
