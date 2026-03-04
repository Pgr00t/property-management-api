from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model representing staff users.
    By default, users registering through the API should be granted staff access,
    or we just rely on IsAuthenticated since the system is staff-only.
    """

    pass
