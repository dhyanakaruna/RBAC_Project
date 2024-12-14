from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True)
    resource = models.CharField(max_length=100)
    action = models.CharField(max_length=50)

    def __str__(self):
        return f"Permission: {self.name}, Action: {self.action}, Resource: {self.resource}"

class User(AbstractUser):
    roles = models.ManyToManyField('Role', related_name='users')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='rbac_users',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='rbac_users',
        blank=True,
    )

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    resource = models.CharField(max_length=255)
    outcome = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.outcome}"