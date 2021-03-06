# -*- coding: utf-8 -*-
import os
import requests
import base64
from xml.etree import ElementTree
from django.core.management.base import BaseCommand
from django.conf import settings
from sights.models import MedJellyBeach


class Command(BaseCommand):
    help = "Import beaches from MedJelly API to MedJellyBeach model"
    enviroment = "production"

    def handle(self, *args, **options):
        url = os.path.join(
            settings.MEDJELLY_API[self.enviroment]["url"],
            "beaches/locations"
        )
        headers = {
            "Authorization": self._auth_string()
        }

        print "GET %s" % url
        response = requests.get(url, headers=headers)

        print "Importing..."
        count = self._import_beaches(response.json())
        print "Imported", count, "beaches"


    def _auth_string(self):
        # TODO: Refactor this into a class wrapping MedJellyAPI, and use it here and in APIExporter
        username = settings.MEDJELLY_API[self.enviroment]["user"]
        password = settings.MEDJELLY_API[self.enviroment]["password"]
        return "Basic %s" % base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    def _import_beaches(self, data):
        count = 0
        for beach in data["beaches"]:
            try:
                medjelly_beach = MedJellyBeach.objects.get(id=beach["id"])
            except MedJellyBeach.DoesNotExist:
                medjelly_beach = MedJellyBeach.objects.create(
                    id=beach["id"],
                    name=beach["name"],
                    town=beach["municipalityName"]
                    )
                count += 1

            if beach["name"] != medjelly_beach.name:
                print medjelly_beach, "ha cambiado de nombre a", beach["name"]
                print "El cambio no se ha aplicado y queda pendiente de revisión manual"

            if beach["municipalityName"] != medjelly_beach.town:
                print medjelly_beach, "ha cambiado de ciudad a", beach["municipalityName"]
                print "El cambio no se ha aplicado y queda pendiente de revisión manual"

        return count
