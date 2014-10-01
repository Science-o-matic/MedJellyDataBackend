# -*- coding: utf-8 -*-
import csv
from django.core.management.base import BaseCommand, CommandError
from sights.models import Sight, Variable, SightVariables


# This intended to be a one-shot management command exporting sights data
# in a fixed format requested by customer. Some hardcoding around here.
class Command(BaseCommand):
    args = 'csvfile'
    help = 'Export all sights in a CSV file'
    metereology_group_name = "Meteorología"
    water_temperature_type = "Temperatura de l'aigua"
    groundswell_presence_type = "Mar de fondo (presencia)"
    sea_status_type = "Estado de la Mar"

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("Path of CSV file to be created has to be passed as first argument")

        with open(args[0], 'wb') as csvfile:
            print "Exporting..."
            csvwriter = csv.writer(csvfile, delimiter=',')
            self.write_header(csvwriter)

            i = 0
            for sighting in Sight.objects.all():
                self.write_sighting(csvwriter, sighting)
                i += 1
            print "Exported", i, "sights"


    def write_header(self, csvwriter):
        header_cols = ["Municipio", "Nombre playa", "Fecha", "Hora", "Presencia Medusas",
                       "Especie / Tamaño / Abundancia", "Meteorología",
                       "Estado de la mar (1 = Plana, 2 = Rizada, 3 = Marejadilla, 4 = Marejada, 5 = Fuerte marejada, 6 = Mar gruesa)",
                       "Presencia Mar de Fondo",
                       "Bandera estado mar (0 = Sin información, 1 = Bandera verde, 2 = Bandera amarilla, 3 = Bandera roja)",
                       "Tª agua", "Reportado por",
                       "Comentarios"]
        csvwriter.writerow(header_cols)


    def write_sighting(self, csvwriter, sighting):
        data = []
        date = sighting.timestamp

        data = [sighting.beach.city, sighting.beach, date.strftime("%d/%m/%Y"),
                date.strftime("%H:%M"), int(sighting.jellyfishes_presence),
                self._get_jellyfishes(sighting),
                ",".join(self._get_metereology_variables_values(sighting)),
                self._get_sea_status(sighting),
                self._get_groundswell_presence(sighting),
                sighting.get_flag(),
                sighting.get_water_temp() or "N/A",
                sighting.reported_from,
                sighting.comments
                ]

        csvwriter.writerow([unicode(s).encode("utf-8") for s in data])


    def _get_jellyfishes(self, sighting):
        jellyfishes = ""

        for jellyfish in sighting.jellyfishes.all():
            jellyfishes += "%s / %s / %s |" % (
                jellyfish.jellyfish.name,
                jellyfish.size.id,
                jellyfish.abundance.id
            )

        return jellyfishes

    def _get_metereology_variables_values(self, sighting):
        metereology_variables = sighting.get_variables_by_group_name(self.metereology_group_name)
        return metereology_variables.values_list(
            "variable__label",
            flat=True
        )

    def _get_groundswell_presence(self, sighting):
        try:
            value = sighting.get_variable_by_type(self.groundswell_presence_type)[0].value
        except IndexError:
            value = 0
        return value

    def _get_sea_status(self, sighting):
        try:
            value = sighting.get_variable_by_type(self.sea_status_type)[0].value
        except IndexError:
            value = ""
        return value
