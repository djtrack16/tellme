from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User)
    date_of_born = models.DateField(_('Date of born'), null=True, blank=True)
    photo = models.ImageField(_('Photo'), upload_to='profiles', null=True, blank=True)

    def get_full_name(self):
        return self.user.get_full_name() or self.user.username

    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
