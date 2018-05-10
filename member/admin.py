# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Member, Don, Campagne, Competence

class DonInline(admin.TabularInline):
    model = Don
    extra = 1

class SkillInline(admin.StackedInline):
    model = Member.competences.through
    extra = 1

class MemberAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('nom', 'prenom'), ('email', 'telephone'), ('adherent', 'donateur', 'benevole', 'militant', 'activiste')),
        }),
        ('Adresse', {
            'fields': ('adresse', ('code_postal', 'ville', 'pays')),
            'classes': ('collapse'),
        }),
        (None, {
            'fields': (
                ['commentaire']),
        }),
        (None, {
            'fields': (
            ['competences']),
        }),
    )
    list_display = ('nom', 'prenom', 'email', 'adherent', 'donateur', 'benevole', 'militant', 'activiste')
    list_editable = ('adherent', 'donateur', 'benevole', 'militant', 'activiste')
    filter_horizontal = ['competences']
    inlines = [ DonInline ]

class DonAdmin(admin.ModelAdmin):
    list_display = ('date', 'montant', 'prenom_member', 'nom_member', 'mail_member')
    # list_display = ('date', 'montant')
    actions_on_bottom = True
    def prenom_member(self, obj):
        return (obj.member.prenom)
    prenom_member.short_description = 'Prenom'

    def nom_member(self, obj):
        return (obj.member.nom)
    nom_member.short_description = 'Nom'

    def mail_member(self, obj):
        return (obj.member.email)
    mail_member.short_description = 'mail'

# Register your models here.
admin.site.register(Member, MemberAdmin)
admin.site.register(Don, DonAdmin)
admin.site.register(Campagne)
admin.site.register(Competence)
