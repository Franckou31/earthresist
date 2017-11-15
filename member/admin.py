# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Member, Don, Campagne

class DonInline(admin.TabularInline):
    model = Don

class MemberAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('nom', 'prenom'), ('email', 'telephone'), ('adherent', 'benevole')),
        }),
        ('Adresse', {
            'fields': ('adresse', ('code_postal', 'ville', 'pays')),
            'classes': ('collapse'),
        }),
    )
    list_display = ('nom', 'prenom', 'email')
    inlines = [ DonInline ]
# Register your models here.
admin.site.register(Member, MemberAdmin)
admin.site.register(Don)
admin.site.register(Campagne)
