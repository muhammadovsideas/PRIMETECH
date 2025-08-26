from django.db import models
from django.contrib.auth.models import AbstractUser


# ------------------ Custom User (Admin & Manager) ------------------
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"

    role = models.CharField(max_length=20, choices=Role.choices)
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name} ({self.role})"

