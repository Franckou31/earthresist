# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from member.models import Campagne, Member, Don
from datetime import datetime
import csv


# https://stackoverflow.com/questions/904041/reading-a-utf8-csv-file-with-python
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(unicode_csv_data,
                            dialect=dialect, **kwargs)
    row_number = 0
    for row in csv_reader:
        row_number += 1
        # decode iso-8859-1 back to Unicode, cell by cell:
        if row_number > 1:
            yield [unicode(cell, 'iso-8859-1') for cell in row]


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


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
            new_member.nom = row[18]
            new_member.prenom = row[19]
            new_member.adresse = row[20]
            new_member.code_postal = row[21]
            new_member.ville = row[22]
            new_member.pays = row[23]
            self.stdout.write(row[2])
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

            id_hello_asso = int(member[0])
            dons = Don.objects.filter(num_hello_asso=id_hello_asso)
            if dons.count() == 0:
                don = Don()
                don.num_hello_asso = int(member[0])
                don.origin_don = "HelloAsso"
                don.campagne = campaign
                don.type_don = member[2]
                don.date = datetime.strptime(member[3][0:10], '%d/%m/%Y')
                don.montant = int(member[4])
                don.attestation_hello_asso = member[5]
                don.type_paiement = "HA"
                don.member = user

                don.save()



    def add_arguments(self, parser):
        parser.add_argument('csvfile')

    def handle(self, *args, **options):
        import_file = options['csvfile']
        self.stdout.write('csvfile ' + import_file)
        with open(import_file) as f:
            row = unicode_csv_reader(f, delimiter=';')
            self.process_row(row)
