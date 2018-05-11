# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date


class Campagne(models.Model):
    nom = models.CharField(max_length=200)
    date = models.DateField(default=date.today)
    def __str__(self):
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
        (u'Adhésion', u'Adhésion'),
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

class Competence(models.Model):
    nom = models.CharField(max_length=50)
    def __str__(self):
        return str(self.nom)

class Member(models.Model):
    class Meta:
        permissions = (
            ("can_only_change_comment", "Can only change comment"),
        )
    CIVILITE = (
        ('Mme', 'Madame'),
        ('Mr', 'Monsieur'),
    )
    # infos generale
    civilite = models.CharField(blank=True, max_length=10, choices=CIVILITE)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    # type membre
    adherent = models.BooleanField(default=False)
    benevole = models.BooleanField(default=False)
    donateur = models.BooleanField(default=False)
    militant = models.BooleanField(default=False)
    activiste = models.BooleanField(default=False)
    # newletter O/N
    newsletter = models.BooleanField(default=False)
    # Informer prochaines actions O/N
    informaction = models.BooleanField(default=False)
    # Adresse
    adresse = models.TextField(blank=True)
    code_postal = models.CharField(max_length=5, blank=True)
    ville = models.CharField(max_length=50, blank=True)
    pays = models.CharField(max_length=50, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    # Competence
    competences = models.ManyToManyField(Competence, blank=True)
    # Date lieu creation membre
    campagne = models.ForeignKey(
        'Campagne',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    commentaire = models.TextField(blank=True)

    def __unicode__(self):
        return self.prenom + " " + self.nom

