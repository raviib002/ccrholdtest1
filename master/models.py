from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from audit_log.models.fields import CreatingUserField, LastUserField
from django.db.models.deletion import CASCADE
from random import choices

# Create your models here.
class News(models.Model):
    news_headline = models.CharField(max_length=250, verbose_name=_("News Headline"))
    photo = models.ImageField(upload_to='News_photo/', default='', verbose_name=_("News Photo"))
    desc  = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    created_by = CreatingUserField(related_name = "NewsCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "NewsUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.news_headline
    
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        db_table = 'ccrh_news'
        

class Downloads(models.Model):
    download_headline = models.CharField(max_length=250, verbose_name=_("Download Headline"))
    desc  = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    created_by = CreatingUserField(related_name = "DownloadsCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "DownloadsUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.download_headline
    
    class Meta:
        verbose_name = "Downloads"
        verbose_name_plural = "Downloads"
        db_table = 'ccrh_downloads'
        

class QuickLink(models.Model):
    headline = models.CharField(max_length=250, verbose_name=_("Quick Link Headline"))
    photo = models.ImageField(upload_to='QuickLink_photo/', default='', verbose_name=_("Quick Link Banner"))
    link  = models.URLField(verbose_name=_("URL"))
    created_by = CreatingUserField(related_name = "QuickLinkCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "QuickLinkUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.headline
    
    class Meta:
        verbose_name = "QuickLink"
        verbose_name_plural = "QuickLink"
        db_table = 'ccrh_quick_link'
        
class Media(models.Model):
    headline = models.CharField(max_length=250, verbose_name=_("Media Headline"))
    cover_photo = models.ImageField(upload_to='Media_cover/', default='', verbose_name=_("Quick Link Banner"))
    video  = models.FileField(upload_to='Media_video', verbose_name=_("Video"))
    created_by = CreatingUserField(related_name = "MediaCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "MediaUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.headline
    
    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media"
        db_table = 'ccrh_media'
        
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
        
