from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from account.views import SignupView, LoginView, LogoutView, DeleteView
from account.views import ConfirmEmailView
from account.views import ChangePasswordView, PasswordResetView, PasswordResetTokenView
from account.views import SettingsView

from scraper_monitor.views import monitor_scraper, stop_spider, start_spider


urlpatterns = [
    url(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    url(r"^account/login/$", LoginView.as_view(), name="account_login"),
    url(r"^account/logout/$", LogoutView.as_view(), name="account_logout"),
    url(r"^account/confirm_email/(?P<key>\w+)/$", ConfirmEmailView.as_view(), name="account_confirm_email"),
    url(r"^account/password/$", ChangePasswordView.as_view(), name="account_password"),
    url(r"^account/password/reset/$", PasswordResetView.as_view(), name="account_password_reset"),
    url(r"^account/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$", PasswordResetTokenView.as_view(), name="account_password_reset_token"),
    # url(r"^account/settings/$", SettingsView.as_view(), name="account_settings"),
    # url(r"^account/delete/$", DeleteView.as_view(), name="account_delete"),
]


urlpatterns += [
    url(r"^$", monitor_scraper, name="home"),
    url(r"^start/$", start_spider, name="start_spider"),
    url(r"^stop/$", stop_spider, name="stop_spider"),
    url(r"^admin/", include(admin.site.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
