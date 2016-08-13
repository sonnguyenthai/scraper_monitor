from django.contrib import admin

from scraper_monitor.models import Scraper

class ScraperAdmin(admin.ModelAdmin):
    exclude = ('job_id', 'date_created', 'date_modified')
    list_display = ('name', 'host', 'port', 'spider_name', 'scraper_project_name')

admin.site.register(Scraper, ScraperAdmin)