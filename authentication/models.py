
from django.contrib.auth.models import AbstractUser
from django.db import models
import phonenumbers
from django.core.exceptions import ValidationError


# Create your models here.

class User(AbstractUser):
    ADMIN  = 'ADMIN'
    STAFF  = 'STAFF'
    CLIENT = 'CLIENT'

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (CLIENT, 'Client'),
    )
    
    # phone = models.CharField(max_length=20, verbose_name='Numéro de téléphone', unique=True)
    email = models.EmailField(unique=True, verbose_name='Adresse email', error_messages={'required': 'Veuillez renseigner votre adresse email.'})
    phone = models.CharField(unique=True, max_length=20, verbose_name='Numéro de téléphone',
        error_messages={'required': 'Veuillez renseigner votre numéro de téléphone.'}
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle', default='CLIENT')
    
    def fullname(self) -> str:
        return self.first_name + " " + self.last_name
    
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='Nom de l\'adresse')
    fullname = models.CharField(max_length=255, verbose_name='Nom')
    company = models.CharField(max_length=128, blank=True, verbose_name='Société')
    address = models.TextField(verbose_name='Adresse')
    addressComplement = models.CharField(max_length=255, blank=True, verbose_name='Complément adresse')
    zip = models.CharField(max_length=10, verbose_name='Code postal')
    city = models.CharField(max_length=64, verbose_name='Ville')
    country = models.CharField(max_length=64, verbose_name='Pays')
    phone = models.CharField(max_length=20, verbose_name='Numéro de téléphone',
        error_messages={'required': 'Veuillez renseigner votre numéro de téléphone.'}
    )
    
    def __str__(self):
        components = [self.fullname, self.address]

        if self.addressComplement:
            components.append(self.addressComplement)

        location_info = f"{self.zip} {self.city}, {self.country}"
        components.append(location_info)

        return ', '.join(components)