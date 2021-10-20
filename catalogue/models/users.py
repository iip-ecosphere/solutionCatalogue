from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from catalogue.models.component import Component


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    company = models.CharField("Unternehmen", max_length=100, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def component_count(self) -> int:
        return Component.objects.filter(created_by=self.user).count()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs) -> None:
    if created:
        # add user profile
        Profile.objects.create(user=instance)
        # add user to default group
        group = Group.objects.get(name="Autoren")
        instance.groups.add(group)
    instance.profile.save()


@receiver(pre_save, sender=User)
def add_to_staff(sender, instance, **kwargs) -> None:
    instance.is_staff = True
