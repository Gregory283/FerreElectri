from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog
from django.contrib.auth.models import User
from FERREELECTRI_PLUS.middleware import get_current_user

@receiver(post_save)
def log_save_signal(sender, instance, created, **kwargs):
    if sender not in [AuditLog, User]:
        action = "CREAR" if created else "ACTUALIZAR"
        user = get_current_user()
        AuditLog.objects.create(
            user=user if user else None,
            action=action,
            model_name=sender.__name__,
            object_id=instance.pk,
            details=str(instance)
        )

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender != AuditLog:
        AuditLog.objects.create(
            user=get_current_user(),
            action="ELIMINAR",
            model_name=sender.__name__,
            object_id=instance.pk,
            details=str(instance)
        )