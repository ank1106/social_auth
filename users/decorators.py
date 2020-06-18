from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


def user_is_admin(function):
    def wrap(self, *args, **kwargs):
        if isinstance(self.request.user, User):
            if self.request.user.is_superuser and self.request.user.is_staff and self.request.user.is_authenticated:
                return function(self, *args, **kwargs)
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
