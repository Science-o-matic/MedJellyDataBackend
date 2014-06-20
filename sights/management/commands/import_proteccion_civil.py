# -*- coding: utf-8 -*-
import requests
from datetime import datetime
import logging
from datetime import date, datetime
from collections import defaultdict
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from sights.models import Sight, ReportingClient, Beach, SightVariables, SightJellyfishes, \
    Jellyfish


logger = logging.getLogger(__name__)


# Colums to be retrieved from Protección Civíl's API
API_COLUMNS = {
    'all': ("CodiPlatja", "Data", "Bandera", "Meduses", "Meteorologia",
            "EstatMar", "MarDeFons", "Temperatura"),
    'variables': ("Bandera", "Meteorologia", "EstatMar", "MarDeFons", "Temperatura"),
    'jellyfishes': "Meduses"
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
    "EstatMar": {
        "id": 68,
        "value": {
            "plana": 1,
            "arrissada": 2,
            "marejol": 3,
            "maror": 4,
            "forta maror": 5,
            "maregassa": 6,
         }
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

JELLYFISH_CONVERSION = {
    "abundance": {
        "poques": 1,
        "bastants": 2,
        "moltes": 3
    },
    "size": {
        "0-5": 1,
        "5-10": 2,
        "10-15": 3,
        "15-25": 4,
        ">25": 5
    }
}


class Command(BaseCommand):
    help = 'Import sightings data from "Protección Civil" Google Fusion Table'
    reporting_client_id = 2
    datetime_format = "%d/%m/%y %H:%M"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        try:
            # Protección Civíl reporting client
            self.reporting_client = ReportingClient.objects.get(
                id=self.reporting_client_id
            )
        except ReportingClient.DoesNotExist:
            message = "No reporting client with id=%s found!" % self.reporting_client_id
            logger.critical(message)
            raise CommandError(message)

    def handle(self, *args, **options):
        last_import_date = self.reporting_client.last_import_date
        if not last_import_date:
            logger.warning("No last import date found, importing sightins from today's date.")
            last_import_date = date.today()

        params = {
            'key': settings.PROTECCION_CIVIL_API['key'],
            'sql': "SELECT %s FROM %s WHERE Data >= '%s'" % (
                ",".join(API_COLUMNS['all']),
                settings.PROTECCION_CIVIL_API['tables']['sightings'],
                last_import_date.strftime(self.datetime_format)
            )
        }

        logger.info("GET %s?%s" % (settings.PROTECCION_CIVIL_API['base_url'], params["sql"]))
        response = requests.get(settings.PROTECCION_CIVIL_API['base_url'], params=params)
        sightings = response.json()

        if 'rows' in sightings:
            self._import(sightings)
        else:
            logger.info("No new sightings recieved.")

    def _import(self, sightings):
        total = len(sightings['rows'])
        logger.info("Importing %s sightings" % total)

        count = 0
        for s in sightings['rows']:
            sighting = self._prepare_sighting(s, sightings['columns'])
            count += self._create_sighting(sighting)

        self.reporting_client.last_import_date = datetime.today()
        self.reporting_client.save()

        logger.info("Sightings successfully imported: %i, failed: %i" % (count, total - count))

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
            logger.warning("Error converting date %s to DD/MM/YYYY" % sighting["Data"])
            return 0

        try:
            beach = Beach.objects.get(proteccion_civil_api_id=proteccion_civil_beach_id)
        except Beach.DoesNotExist:
            logger.warning("Beach with proteccion_civil_api_id=%s not found!" % proteccion_civil_beach_id)
            return 0

        s, _ = Sight.objects.get_or_create(
            timestamp=date,
            beach=beach,
            reported_from=self.reporting_client
        )

        self._add_sighiting_variables(s, sighting)

        self._add_sighiting_jellyfishes(s, sighting[API_COLUMNS["jellyfishes"]])

        return 1

    def _add_sighiting_variables(self, sighting, sighting_data):
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

    def _add_sighiting_jellyfishes(self, sighting, jellyfishes):
        for jelly in jellyfishes.split(";"):
            name, abundance, size = jelly.split(",")
            SightJellyfishes.objects.get_or_create(
                sight=sighting,
                jellyfish=Jellyfish.objects.get(name__contains=name),
                defaults={
                    "size_id": JELLYFISH_CONVERSION["size"][size],
                    "abundance_id": JELLYFISH_CONVERSION["abundance"][abundance]
                }
            )
