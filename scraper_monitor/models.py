from django.db import models


class Scraper(models.Model):
    """
    Scraper to monitor
    """
    name = models.CharField("Scraper Name", max_length=100, null=True, blank=True)
    host = models.CharField("Host Name", max_length=150, null=False)
    port = models.IntegerField("Port", null=False)
    spider_name = models.CharField("Spider Name", max_length=100, null=True, default="delcampe.net")
    scraper_project_name = models.CharField("Scraper Project Name", max_length=100, null=True, default="delcampe")
    job_id = models.CharField("Job ID", max_length=150, null=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    @property
    def ws_url(self):
        return "http://%s:%s" % (self.host, self.port)

    @property
    def show_name(self):
        if self.name:
            return self.name
        else:
            return self.ws_url
