from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Automatically set all new users to be staff...
@receiver(pre_save, sender=User)
def auto_set_staff(sender, instance, **kwargs):
  if not instance.pk:
    instance.is_staff = True
