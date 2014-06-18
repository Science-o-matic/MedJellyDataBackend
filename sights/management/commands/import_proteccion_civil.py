# -*- coding: utf-8 -*-
import requests
from datetime import datetime
from collections import defaultdict
from django.core.management.base import BaseCommand
from django.conf import settings
from sights.models import Sight, ReportingClient, Beach, SightVariables

# Colums to be retrieved from Protección Civíl's API
API_COLUMNS = {
    'all': ("CodiPlatja", "Data", "Bandera", "Meduses", "Meteorologia",
            "EstatMar", "MarDeFons", "Temperatura"),
    'variables': ("Bandera", "Meteorologia", "EstatMar", "MarDeFons", "Temperatura"),
    'jellyfishes': ("Meduses",)
}

# Conversion from Protección Civil's api rows to variables ids
VARIABLE_CONVERSION = {
    "Bandera": {
        "id": 67,
        "value": {
            "sense informació": 0,
            "verda": 1,
            "groga": 2,
            "vermella": 3
            }
    },
    "Meteorologia": {
        "id": {
            "sol": 44,
            "ennuvolat": 43,
            "pluja": 45,
            "xáfecs": 64
        },
        "value": defaultdict(lambda: True),
    },
    "MarDeFons": {
        "id": 40,
        "value": {
            "si": True,
            "no": False
        }
    },
    "Temperatura": {
        "id": 63,
    },
}


class Command(BaseCommand):
    help = 'Import sightings data from "Protección Civil" Google Fusion Table'

    def handle(self, *args, **options):
        params = {
            'key': settings.PROTECCION_CIVIL_API['key'],
            'sql': "SELECT %s FROM %s WHERE Data > %s LIMIT 50" % (
                ",".join(API_COLUMNS['all']),
                settings.PROTECCION_CIVIL_API['tables']['sightings'],
                "'01/06/2014'"
            )
        }

        print "GET %s?%s" % (settings.PROTECCION_CIVIL_API['base_url'], params["sql"])
        response = requests.get(settings.PROTECCION_CIVIL_API['base_url'], params=params)
        sightings = response.json()

        total = len(sightings['rows'])
        print "Recieved %i sightings." % total
        print "Importing..."
        count = 0
        for s in sightings['rows']:
            sighting = self._prepare_sighting(s, sightings['columns'])
            count += self._create_sighting(sighting)
        print "Sightings imported:", count, "failed:", total - count

    def _prepare_sighting(self, sighting, cols):
        prepared_sighting = {}
        for i, col in enumerate(cols):
            prepared_sighting[col] = sighting[i]
        return prepared_sighting

    def _create_sighting(self, sighting):
        proteccion_civil_beach_id = sighting["CodiPlatja"]

        try:
            date = datetime.strptime(sighting["Data"], '%d/%m/%Y %H:%M')
            date = date.strftime('%Y-%m-%d %H:%M')
        except ValueError:
            print "Error converting date %s to DD/MM/YYYY" % sighting["Data"]
            return 0

        try:
            beach = Beach.objects.get(proteccion_civil_api_id=proteccion_civil_beach_id)
        except Beach.DoesNotExist:
            print "Beach with proteccion_civil_api_id=%s not found!" % proteccion_civil_beach_id
            return 0

        reported_from = ReportingClient.objects.get(id=2) # Protección Civíl

        s, _ = Sight.objects.get_or_create(
            timestamp=date,
            beach=beach,
            reported_from=reported_from
        )
        self._add_sighitings_variables(s, sighting)
        return 1

    def _add_sighitings_variables(self, sighting, sighting_data):
        for key in API_COLUMNS['variables']:
            try:
                variable_id = self._variable_id(key, sighting_data[key])
                value = self._convert_value(key, sighting_data[key])
            except:
                continue

            try:
                sv = SightVariables.objects.get(
                    sight=sighting,
                    variable_id=variable_id
                )
            except SightVariables.DoesNotExist:
                SightVariables.objects.create(
                    sight=sighting,
                    variable_id=variable_id,
                    value=value
                )


    def _variable_id(self, key, value):
        try:
            variable_converted = VARIABLE_CONVERSION[key]
        except KeyError:
            print "Variable named %s not found!" % key
            return

        variable_id = variable_converted["id"]
        if isinstance(variable_id, dict):
            return variable_id[value]
        else:
            return variable_id

    def _convert_value(self, key, value):
        try:
            conversion = VARIABLE_CONVERSION[key]
        except KeyError:
            print "Conversion for variable %s not found!" % key
            raise

        try:
            value_conversion = conversion["value"]
        except KeyError:
            return value

        try:
            return value_conversion[value]
        except KeyError:
            print "Conversion for %s=%s not found!" % (key, value)
            raise
