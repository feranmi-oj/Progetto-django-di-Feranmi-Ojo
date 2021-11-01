from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    birthday = models.DateField(blank=True,null=True)
    ip_address = models.CharField(max_length=150, blank=True,null=True)

    def __str__(self):
        return "Profilo dell'utente {}".format(self.user.username)
    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'id':self.id})

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

