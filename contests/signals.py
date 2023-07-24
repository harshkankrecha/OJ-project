from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from .tasks import schedule_contest


@receiver(post_save, sender=Contest)
def save_contest_to_model(sender, instance, created, **kwargs):
    schedule_contest(instance.id)