import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "poc_django_reactjs.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import poc_django_reactjs.users.signals  # noqa: F401
