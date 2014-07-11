# -*- coding: utf-8 -*-
import requests
from datetime import datetime
import logging
from datetime import date, datetime
from collections import defaultdict
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from sights.models import Sight, ReportingClient, Beach, SightVariables, SightJellyfishes, \
    Jellyfish, ProteccionCivilBeach
from sights import mailer

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
            "sense informacio": 0,
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
    datetime_format = "%Y-%m-%d %H:%M:%S"
    report = {"received": 0, "imported": 0, "failed": 0,
              "having_jellyfishes": 0, "not_having_jellyfishes": 0,
              "not_found_beaches": [],
              "sightings_having_jellyfishes": []}

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
            'sql': "SELECT %s FROM %s WHERE Data > '%s' ORDER BY Data" % (
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
            mailer.notify_import_report(self.report)
        else:
            logger.info("No new sightings recieved.")

    def _import(self, sightings):
        received = len(sightings['rows'])

        imported = 0
        last_date = None
        for s in sightings['rows']:
            sighting = self._prepare_sighting(s, sightings['columns'])
            sighting_created = self._create_sighting(sighting)
            if sighting_created:
                imported +=1
                last_date = sighting_created.timestamp

        if last_date:
            self.reporting_client.last_import_date = last_date
            self.reporting_client.save()

        self.report["received"] = received
        self.report["imported"] = imported
        self.report["failed"] = received - imported
        self.report["not_having_jellyfishes"] = imported - self.report["having_jellyfishes"]
        logger.info("Received %(received)s sightings, imported: %(imported)s, failed: %(failed)s" %
                    self.report)

    def _prepare_sighting(self, sighting, cols):
        prepared_sighting = {}
        for i, col in enumerate(cols):
            prepared_sighting[col] = sighting[i]
        return prepared_sighting

    def _create_sighting(self, sighting):
        proteccion_civil_beach_id = sighting["CodiPlatja"]

        date = datetime.strptime(sighting["Data"], self.datetime_format)

        try:
            beach = Beach.objects.get(
                proteccion_civil_beaches__code__in=[proteccion_civil_beach_id]
            )
        except Beach.DoesNotExist:
            self._log_sighting_warning(
                "Beach with proteccion_civil_api_id=%s not found!" % proteccion_civil_beach_id,
                sighting
            )
            self._report_not_found_beach(proteccion_civil_beach_id)
            return None

        sighting_instance, created = Sight.objects.get_or_create(
            timestamp=date,
            beach=beach,
            reported_from=self.reporting_client
        )

        if created:
            self._add_sighting_variables(sighting_instance, sighting)
            self._add_sighting_jellyfishes(sighting_instance, sighting[API_COLUMNS["jellyfishes"]])

            if sighting_instance.jellyfishes_presence:
                self.report["having_jellyfishes"] += 1
                self.report["sightings_having_jellyfishes"].append(sighting_instance.id)
            return sighting_instance
        else:
            return None

    def _add_sighting_variables(self, sighting, sighting_data):
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
            logger.warning("Variable named %s not found!" % key)
            return

        variable_id = variable_converted["id"]
        if isinstance(variable_id, dict):
            return variable_id[value]
        else:
            return variable_id

    def _convert_value(self, key, value):
        if value == "NaN":
            logger.warning("Invalid value (%s=NaN)" % key)
            raise Exception("Invalid value")

        try:
            conversion = VARIABLE_CONVERSION[key]
        except KeyError:
            logger.warning("Conversion for variable %s not found!" % key)
            raise

        try:
            value_conversion = conversion["value"]
        except KeyError:
            return value

        try:
            return value_conversion[value]
        except KeyError:
            logger.warning("Conversion for %s=%s not found!" % (key, value))
            raise

    def _add_sighting_jellyfishes(self, sighting, jellyfishes):
        if not jellyfishes:
            return

        for jelly in jellyfishes.split(";"):
            name, abundance, size = jelly.split(",")

            try:
                jellyfish = Jellyfish.objects.get(name__contains=name)
            except Jellyfish.DoesNotExist:
                logger.warning("Jellyfish named %s not found!" % name)

            SightJellyfishes.objects.create(
                sight=sighting,
                jellyfish=jellyfish,
                size_id=JELLYFISH_CONVERSION["size"][size],
                abundance_id=JELLYFISH_CONVERSION["abundance"][abundance]
            )

    def _log_sighting_warning(self, message, sighting):
        logger.warning("[sighting %s] %s" % (sighting["Data"], message))

    def _report_not_found_beach(self, code):
        try:
            proteccion_civil_beach = ProteccionCivilBeach.objects.get(code=code)
        except ProteccionCivilBeach.DoesNotExist:
            proteccion_civil_beach = code
        self.report["not_found_beaches"].append(proteccion_civil_beach)
