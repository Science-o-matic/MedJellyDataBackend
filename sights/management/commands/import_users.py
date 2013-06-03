import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    args = 'csvfile'
    help = 'Parse csvfile creating users'

    def handle(self, *args, **options):
        file = open(args[0])
        csvReader = csv.reader(file)
        for row in csvReader:
            name, username = row[1].strip()[:29], row[2].strip()
            User.objects.get_or_create(username=username, first_name=name)
