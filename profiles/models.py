from django.db import models
from django.conf import settings
from phone_field import PhoneField
# Create your models here.
def upload_update_image(instance , filename):
    return "profile/{user}/{filename}/".format(user=instance.user , filename=filename)

class ProfileQuerySet(models.QuerySet):
    pass 

class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model , using=self._db)

class Profile(models.Model):
    user        =models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, null=False)
    phone     =PhoneField(blank=True, help_text='Contact phone number')
    image       =models.ImageField(upload_to=upload_update_image , blank=True , null=True)
    typeOf     =models.CharField(max_length = 10)
    organization   =models.CharField(max_length = 80, blank=True , null=True)
    about   =models.CharField(max_length = 380, blank=True , null=True)
    pubInterest     =models.TextField(blank=True , null=True)
    authInterest     =models.TextField(blank=True , null=True)
    
    objects = ProfileManager()

    # def __str__(self):
    #     return str(self.about)[:50]

    class Meta:
        verbose_name = 'Profile post'
        verbose_name_plural = 'Profile posts'

    @property
    def owner(self):
        return self.user
