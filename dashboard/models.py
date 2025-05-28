from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=255, null=True, blank=True)  # Cambiado a CharField
    timestamp = models.DateTimeField(default=now)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action} - {self.model_name} - {self.timestamp}"

