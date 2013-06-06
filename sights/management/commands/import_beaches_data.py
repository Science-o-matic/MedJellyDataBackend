import csv
from django.core.management.base import BaseCommand
from sights.models import Beach, City, BeachOwner


class Command(BaseCommand):
    args = 'csvfile'
    help = 'Parse csvfile creating beachs'

    def handle(self, *args, **options):
        file = open(args[0])
        csvReader = csv.reader(file)
        for row in csvReader:
            beach = {
                "code": row[0].strip(),
                "city": row[2].strip(),
                "name": row[3].strip(),
                "owner": row[4].strip()
            }

            # Sorry for this, but is a one-shot script and it's late :-)
            exists = True
            try:
                beach_object = Beach.objects.get(name__endswith=beach["name"])
            except:
                try:
                    shorted_name = " ".join(beach["name"].split(" ")[1:])
                    beach_object = Beach.objects.get(name__contains=shorted_name)
                except:
                    try:
                        shorted_name = " ".join(beach["name"].split(" ")[2:])
                        beach_object = Beach.objects.get(name__contains=shorted_name)
                    except:
                        exists = False
                        print beach["code"], beach["name"]
            if exists:
                beach_object.city, _ = City.objects.get_or_create(name=beach["city"])
                beach_object.owner, _ = BeachOwner.objects.get_or_create(name=beach["owner"])
                beach_object.save()
