# -*- coding: utf-8 -*-
import csv
from django.core.management.base import BaseCommand
from sights.models import Beach, MedJellyBeach, ProteccionCivilBeach, City


class Command(BaseCommand):
    help = "Generates a report about correspondences between Beach, MedJellyBeach and ProteccionCivilBeach"

    def handle(self, *args, **options):
        self._generate_beaches_report()
        self._generate_medjelly_beaches_report()
        self._generate_proteccion_civil_beaches_report()


    def _generate_beaches_report(self):
        report = [("Id Playa", "Nombre Playa", "Nombre Playa MedJelly", u"Nombre Playa Protección Civíl",
                  "Id Medjelly", u"Id Protección Civíl"),]

        for beach in Beach.objects.all():
            medjelly_beach = self._get_medjelly_beach(beach)
            proteccion_civil_beach = self._get_proteccion_civil_beach(beach)

            beach_city = self._get_beach_city(beach)

            report.append((
                    unicode(beach.id),
                    "%s (%s)" % (beach.name, beach_city),
                    "%s (%s)" % (medjelly_beach.name, medjelly_beach.town),
                    "%s (%s)" % (proteccion_civil_beach.name, proteccion_civil_beach.town),
                    unicode(medjelly_beach.id),
                    unicode(proteccion_civil_beach.code or '')
                    ))

        with open('beaches.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for line in report:
                writer.writerow([c.encode("utf-8") for c in line])

    def _generate_medjelly_beaches_report(self):
        report = [("Nombre Playa MedJelly", "Nombre Playa",
                  "Id Medjelly", "Id Playa"),]

        for medjelly_beach in MedJellyBeach.objects.all():
            beach = self._get_beach(medjelly_api_id=medjelly_beach.id)

            report.append(("%s (%s)" % (medjelly_beach.name, medjelly_beach.town),
                           "%s (%s)" % (beach.name, beach.city),
                           unicode(medjelly_beach.id),
                           unicode(beach.id)))

        with open('beaches_medjelly.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for line in report:
                writer.writerow([c.encode("utf-8") for c in line])

    def _generate_proteccion_civil_beaches_report(self):
        report = [(u"Nombre Playa Protección Civíl", "Nombre Playa",
                  "Id Proteccion Civil", "Id Playa"),]

        for proteccion_civil_beach in ProteccionCivilBeach.objects.all():
            beach = self._get_beach(proteccion_civil_api_id=proteccion_civil_beach.code)

            report.append(("%s (%s)" % (proteccion_civil_beach.name, proteccion_civil_beach.town),
                           "%s (%s)" % (beach.name, beach.city),
                           unicode(proteccion_civil_beach.code), unicode(beach.id)))

        with open('beaches_proteccion_civil.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for line in report:
                writer.writerow([c.encode("utf-8") for c in line])


    def _get_beach(self, medjelly_api_id=None, proteccion_civil_api_id=None):
        try:
            if medjelly_api_id:
                beach = Beach.objects.get(medjelly_api_id=medjelly_api_id)
            elif proteccion_civil_api_id:
                beach = Beach.objects.get(proteccion_civil_api_id=proteccion_civil_api_id)
        except Beach.DoesNotExist:
            beach = Beach(id=0, name="")

        beach.city = self._get_beach_city(beach)

        return beach

    def _get_beach_city(self, beach):
        try:
            return beach.city
        except City.DoesNotExist:
            return City(name="N/A")


    def _get_medjelly_beach(self, beach):
        try:
            return MedJellyBeach.objects.get(id=beach.medjelly_api_id)
        except MedJellyBeach.DoesNotExist:
            return MedJellyBeach(id=0, name="")

    def _get_proteccion_civil_beach(self, beach):
        try:
            return ProteccionCivilBeach.objects.get(code=beach.proteccion_civil_api_id)
        except ProteccionCivilBeach.DoesNotExist:
            return ProteccionCivilBeach(code="0", name="")
