import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from sights.models import Sight


class Command(BaseCommand):
    help = 'Import sightings data from "Proteccion Civil" Google Fusion Table'


    def handle(self, *args, **options):
        params = {
            'key': settings.PROTECCION_CIVIL_API['key'],
            'sql': "SELECT CodiPlatja, Data, Bandera, Meduses, Meteorologia, "
            "EstatMar, MarDeFons, Temperatura FROM %(sightings)s LIMIT 2" %
            settings.PROTECCION_CIVIL_API['tables']
        }
        r = requests.get(settings.PROTECCION_CIVL_API['base_url'], params=params)
        sightings = r.json()
        for s in sightings['rows']:
            sighting = self._prepare_sighting(s, sightings['columns'])
            self._create_sighting(sighting)

    def _prepare_sighting(self, sighting, cols):
        prepared_sighting = {}
        for i, col in enumerate(cols):
            prepared_sighting[col] = sighting[i]
        return prepared_sighting

    def _create_sighting(self, sighting):
        ts = datetime.strptime(sighting['Data'], '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M')
        Sight.objects.create(timestamp=ts)
