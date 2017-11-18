# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date

# Create your models here.

class Campagne(models.Model):
    nom = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nom

class Don(models.Model):
    TYPE_PAIEMENT = (
        ('ES', 'Espece'),
        ('CK', 'Cheque'),
        ('HA', 'HelloAsso'),
    )
    TYPE_DON = (
        ('Don unique', 'Don unique'),
        ('Don mensuel', 'Don mensuel'),
        ('Adhesion', 'Adhesion'),
    )
    ORIGIN_DON = (
        ('HelloAsso', 'HelloAsso'),
        ('SiteWeb', 'SiteWeb'),
    )

    num_hello_asso = models.IntegerField(default=0)
    origin_don = models.CharField(blank=True, max_length=10, choices=ORIGIN_DON)
    campagne = models.ForeignKey(
        'Campagne',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    type_don = models.CharField(blank=True, max_length=20, choices=TYPE_DON)
    date = models.DateField(default=date.today)
    montant = models.IntegerField(default=0)
    attestation_hello_asso = models.CharField(blank=True, max_length=300)

    type_paiement = models.CharField(blank=True, max_length=2, choices=TYPE_PAIEMENT)
    member = models.ForeignKey(
        'Member',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.montant)

class Member(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    adherent = models.BooleanField()
    benevole = models.BooleanField()
    adresse = models.TextField()
    code_postal = models.CharField(max_length=5)
    ville = models.CharField(max_length=50)
    pays = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)

    def __unicode__(self):
        return self.prenom + " " + self.nom
