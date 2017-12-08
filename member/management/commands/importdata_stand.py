# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from member.models import Campagne, Member, Don
from datetime import datetime
import csv


class Command(BaseCommand):
    help = 'Ce script importe les membres et les dons'

    def create_campaign(self, campaign):
        campaigns = Campagne.objects.filter(nom=campaign)

        if (campaigns.count() == 0):
            # self.stdout.write('Creation campaign -->' + campaign)
            # create the campaign if not exist
            new_campaign = Campagne(nom=campaign.encode('utf-8'))
            new_campaign.save()
            return new_campaign
        else:
            # self.stdout.write('Campaign ' + campaign + ' already exist')
            return campaigns[0]

    def create_member(self, row):
        email = row[15]
        self.stdout.write('email ' + email )
        members = Member.objects.filter(email=email)

        if (members.count() == 0):
            new_member = Member()
            new_member.email = email
            new_member.nom = row[9]
            new_member.prenom = row[8]
            new_member.adresse = row[11]
            new_member.code_postal = row[12]
            new_member.ville = row[13]
            new_member.pays = row[14]
            if(row[2] == u'Adhésion'):
                self.stdout.write('oui')
                new_member.adherent = True
            else:
                self.stdout.write('non')
                new_member.adherent = False
            new_member.benevole = False

            new_member.save()
            return new_member
        else:
            m = members[0]
            if m.adherent == False and row[2] == u'Adhésion':
                m.adherent = True
                m.save()
            return m


    def process_row(self, row):
        for member in row:
            campaign = self.create_campaign(member[1])
            user = self.create_member(member)

            # Cle pour identifier un don
            type = member[2]
            date_don =  datetime.strptime(member[3][0:10], '%d/%m/%Y')
            montant = member[4]
            email = member[15]

            # On regarde si ce don n'a pas déjà été importé
            dons = Don.objects\
                    .filter(member__email=email)\
                    .filter(montant=montant)\
                    .filter(type_don=type)\
                    .filter(date=date_don)

            if dons.count() == 0:
                # Le don n'existe pas, on l'importe
                don = Don()
                don.origin_don = "SiteWeb"
                don.campagne = campaign
                don.type_don = member[2]
                don.date = date_don
                don.montant = int(member[4])
                if member[6] == 'especes':
                    don.type_paiement = 'ES'
                elif member[6] == 'cheque':
                    don.type_paiement = 'CK'
                else:
                    self.stdout.write('type paiment inconnu ' + member[6])

                don.member = user
                don.save()
            else:
                self.stdout.write('Le don %s de %s existe deja' % (montant, email))

    def add_arguments(self, parser):
        parser.add_argument('csvfile')

    def handle(self, *args, **options):
        import_file = options['csvfile']
        self.stdout.write('csvfile ' + import_file)
        with open(import_file, encoding="iso-8859-1") as f:
            row = csv.reader(f, delimiter=';')
            # skip header
            next(row)
            self.process_row(row)
