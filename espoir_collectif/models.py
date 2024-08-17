from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
   email = models.EmailField(unique=True)


class Cagnotte(models.Model):
    intitule = models.CharField(max_length=200)
    description = models.TextField(blank=True)  
    image = models.ImageField(upload_to='cagnottes/', blank=True, null=True)  
    montant_collecte = models.FloatField(default=0)
    objectif_montant_vise = models.FloatField()
    date_debut = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cagnottes')


class Donateur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True)

class Don(models.Model):
    montant = models.FloatField()
    cagnotte = models.ForeignKey(Cagnotte, on_delete=models.CASCADE, related_name='dons')
    donateur = models.ForeignKey(Donateur, on_delete=models.SET_NULL, null=True, blank=True)

