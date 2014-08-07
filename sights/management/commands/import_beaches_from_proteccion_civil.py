# -*- coding: utf-8 -*-
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from sights.models import Beach, ProteccionCivilBeach


class Command(BaseCommand):
    help = "Import beaches from Proteccion Civíl's API to ProteccionCivilBeach model"

    def handle(self, *args, **options):
        params = {
            'key': settings.PROTECCION_CIVIL_API['key'],
            'sql': "SELECT CodiPlatja, Platja, Municipi FROM %(beaches)s" %
            settings.PROTECCION_CIVIL_API['tables']
        }
        r = requests.get(settings.PROTECCION_CIVIL_API['base_url'], params=params)
        beaches = r.json()

        print "Importing..."
        for b in beaches['rows']:
            self._create_beach(self._prepare_beach(b, beaches['columns']))
        print "Imported!"

    def _prepare_beach(self, beach, cols):
        prepared_beach = {}
        for i, col in enumerate(cols):
            prepared_beach[col] = beach[i]
        return prepared_beach

    def _create_beach(self, beach):
        try:
            pc = ProteccionCivilBeach.objects.get(code=beach["CodiPlatja"])
        except ProteccionCivilBeach.DoesNotExist:
            pc = ProteccionCivilBeach.objects.create(
                    code=beach["CodiPlatja"],
                    name=beach["Platja"],
                    town=beach["Municipi"]
                    )

        if beach["Platja"] != pc.name:
            print pc.name, "ha cambiado de nombre a", beach["Platja"]
            print "El cambio no se ha aplicado y queda pendiente de revisión manual."

        if beach["Municipi"] != pc.town:
            print pc.town, "ha cambiado de nombre a", beach["Municipi"]
            print "El cambio no se ha aplicado y queda pendiente de revisión manual."
