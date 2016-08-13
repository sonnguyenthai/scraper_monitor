from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "scraper_monitor"

    def ready(self):
        import_module("scraper_monitor.receivers")
