from .models import AuditLog

def log_access_attempt(user, action, resource, outcome):
    AuditLog.objects.create(
        user=user,
        action=action,
        resource=resource,
        outcome=outcome
    )
