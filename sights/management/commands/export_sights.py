# -*- coding: utf-8 -*-
import csv
from django.core.management.base import BaseCommand, CommandError
from sights.models import Sight, Variable, SightVariables


# This intended to be a one-shot management command exporting sights data
# in a fixed format requested by customer. Some hardcoding around here.
class Command(BaseCommand):
    args = 'csvfile'
    help = 'Export all sights in a CSV file'
    abundance_keyword = "Abundància"
    presence_keyword = "Presència"
    size_keyword = "Grandària"
    presence_variable_label = "Meduses"
    presence_variable_value = "1.00"
    jellyfishes_names = ["Pelagia", "Aurelia", "Cotylorhiza", "Rhizostoma", "Chrysaora",
                         "Aequorea", "Velella","Physalia", "Mnemiopsis", "Phyllorhiza", "Carybdea"]
    metereology_group_name = "Meteorologia"
    water_temperature_type = "Temperatura de l'aigua"


    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("Path of CSV file to be created has to be passed as first argument")

        with open(args[0], 'wb') as csvfile:
            print "Exporting..."
            csvwriter = csv.writer(csvfile, delimiter=',')
            self.write_header(csvwriter)

            i = 0
            for sight in Sight.objects.all():
                self.write_row(csvwriter, sight)
                i += 1
            print "Exported", i, "sights"


    def write_header(self, csvwriter):
        header_cols = ["id", "beach", "date", "day", "month", "year", "time"]
        header_cols += self.jellyfishes_names
        header_cols += ["%s grandaria" % s for s in self.jellyfishes_names]
        header_cols += ["Origen",
                        "Bandera", "Motivo Bandera",
                        "T. Agua",
                        "Metereologia"]
        csvwriter.writerow(header_cols)


    def write_row(self, csvwriter, sight):
        data = []
        date = sight.timestamp
        try:
            data = [sight.id, sight.beach]
            data += [date.strftime("%m/%d/%Y"), date.day, date.month, date.year, date.strftime("%H:%M")]
            data += self.jellyfish_values(sight)
            data += self.jellyfish_size_values(sight)
            data += [sight.reported_from, int(sight.get_flag()), sight.get_flag_reason()]
            data += [self._get_water_temperature(sight)]
            data += [",".join(self._get_metereology_variables_values(sight))]
        except ValueError as e:
            print "Sight id", sight.id, "has throw exception:", e.message
        csvwriter.writerow([unicode(s).encode("utf-8") for s in data])

    def _get_metereology_variables_values(self, sight):
        metereology_variables = sight.get_variables_by_group_name(self.metereology_group_name)
        metereology_variables_names = metereology_variables.values_list(
            "variable__variable__label",
            flat=True
        )
        return metereology_variables_names

    def _get_water_temperature(self, sight):
        try:
            return sight.get_variable_by_type(self.water_temperature_type).value
        except SightVariables.DoesNotExist:
            return ""
        except SightVariables.MultipleObjectsReturned:
            return "N/A"

    def jellyfish_values(self, sight):
        # 0 - ausencia
        # 1 - presencia con abundancia pocas
        # 2 - presencia con abundancia bastantes
        # 3 - presencia con abundancia muchas
        # NA - sin datos
        if self._jellyfishes_presence(sight):
            values = self.get_jellyfish_values(sight)
        else:
            values = [0 for name in self.jellyfishes_names]

        return values

    def jellyfish_size_values(self, sight):
        if self._jellyfishes_presence(sight):
            values = self.jellyfishes_size(sight)
        else:
            values = [0 for name in self.jellyfishes_names]

        return values

    def _jellyfishes_presence(self, sight):
        sight_has_jellyfishes = sight.sightvariables_set.filter(
            variable__variable__label=self.presence_variable_label,
            value=self.presence_variable_value
        )
        return bool(sight_has_jellyfishes)

    def get_jellyfish_values(self, sight):
        jellyfishes_abundance_vars = sight.sightvariables_set.filter(
            variable__variable__label__contains=self.abundance_keyword
            )
        jellyfishes_abundance_vars = jellyfishes_abundance_vars.values_list(
            "variable__variable__label",
            "value"
            )

        jellyfishes_abundance = {}
        for var in jellyfishes_abundance_vars:
            key = var[0].split("-")[0].split(" ")[0].strip()
            value = int(var[1])
            jellyfishes_abundance[key] = value

        values = []
        for jellyfish_name in self.jellyfishes_names:
            jellyfish_presence = self.jellyfishes_presence(jellyfish_name, sight)
            try:
                if jellyfishes_abundance[jellyfish_name] > 0:
                    value = jellyfishes_abundance[jellyfish_name]
                elif jellyfish_presence:
                    value = "NA"
            except KeyError:
                if jellyfish_presence:
                    value = "NA"
                else:
                    value = 0
            values.append(value)
        return values

    def jellyfishes_size(self, sight):
        jellyfishes_size_vars = sight.sightvariables_set.filter(
            variable__variable__label__contains=self.size_keyword
            )
        jellyfishes_size_vars = jellyfishes_size_vars.values_list(
            "variable__variable__label",
            "value"
            )
        jellyfishes_size = {}
        for var in jellyfishes_size_vars:
            key = var[0].split("-")[0].split(" ")[0].strip()
            value = int(var[1])
            jellyfishes_size[key] = value

        values = []
        for jellyfish_name in self.jellyfishes_names:
            jellyfish_presence = self.jellyfishes_presence(jellyfish_name, sight)
            try:
                if jellyfishes_size[jellyfish_name] > 0:
                    value = jellyfishes_size[jellyfish_name]
                elif jellyfish_presence:
                    value = "NA"
            except KeyError:
                if jellyfish_presence:
                    value = "NA"
                else:
                    value = 0
            values.append(value)
        return values


    def jellyfishes_presence(self, name, sight):
        jellyfishes_presence_vars = sight.sightvariables_set.filter(
            variable__variable__type__contains=name,
            value="1.00",
        )
        jellyfishes_presence_vars = jellyfishes_presence_vars.filter(
            variable__variable__type__contains=self.presence_keyword,
        )
        return bool(jellyfishes_presence_vars)
