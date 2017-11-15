from django.core.management.base import BaseCommand, CommandError    
import csv

# https://stackoverflow.com/questions/904041/reading-a-utf8-csv-file-with-python
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(unicode_csv_data,
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

class Command(BaseCommand):
    help = 'Ce script importe les membres et les dons'

    def add_arguments(self, parser):
        parser.add_argument('csvfile')

    def handle(self, *args, **options):
        import_file = options['csvfile']
        self.stdout.write('csvfile ' + import_file)
        with open(import_file) as f:
            row = unicode_csv_reader(f, delimiter=';')
            for member in row:
                self.stdout.write(member[0] + '-->' + member[1])
