from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.core.validators import FileExtensionValidator
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country_instance = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    state_instance = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Inheriting Abstract User
class AppUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=50)
    phone = models.IntegerField()
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.TextField(max_length=500, blank=True, null=True)
    pincode = models.IntegerField()
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone', 'pincode']


class Content(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=300)
    summary = models.CharField(max_length=60)
    document = models.FileField(upload_to='documents/', validators=[FileExtensionValidator(['pdf'])])
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    categories = TaggableManager()  # using taggit library
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True)
