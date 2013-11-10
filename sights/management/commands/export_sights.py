# -*- coding: utf-8 -*-
import csv
from django.core.management.base import BaseCommand, CommandError
from sights.models import Sight, Variable


# This intended to be a one-shot management command exporting sights data
# in a fixed format requested by customer. Some hardcoding around here.
#
class Command(BaseCommand):
    args = 'csvfile'
    help = 'Export all sights in a CSV file'
    abundance_keyword = "Abundància"
    presence_keyword = "Presència"
    presence_variable_label = "Meduses"
    presence_variable_value = "1.00"
    jellyfishes_names = ["Pelagia", "Aurelia", "Cotylorhiza", "Rhizostoma", "Chrysaora",
                         "Aequorea", "Velella","Physalia", "Mnemiopsis", "Phyllorhiza", "Carybdea"]

    metereology_group_name = "Meteorologia"

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("Path of CSV file to be created has to be passed as first argument")

        with open(args[0], 'wb') as csvfile:
            print "Exporting..."
            csvwriter = csv.writer(csvfile, delimiter=',')
            self.write_header(csvwriter)

            total = Sight.objects.all().count()
            for sight in Sight.objects.all():
                self.write_row(csvwriter, sight)
            print "Exported", total, "sights."


    def write_header(self, csvwriter):
        header_cols = ["beach", "date", "day", "month", "year"]
        header_cols += self.jellyfishes_names
        header_cols += ["Origen", "Bandera", "Motivo Bandera", "Metereologia"]
        csvwriter.writerow(header_cols)


    def write_row(self, csvwriter, sight):
        data = []
        date = sight.timestamp
        try:
            data = [sight.beach, date.strftime("%m/%d/%Y"), date.day, date.month, date.year]
            data += self.jellyfish_values(sight)
            data += [sight.reported_from, int(sight.get_flag()), sight.get_flag_reason()]
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


    def jellyfish_values(self, sight):
        # 0 - ausencia
        # 1 - presencia con abundancia pocas
        # 2 - presencia con abundancia bastantes
        # 3 - presencia con abundancia muchas
        # NA - sin datos

        sight_has_jellyfishes = sight.sightvariables_set.filter(
            variable__variable__label=self.presence_variable_label,
            value=self.presence_variable_value
        )
        jellyfishes_presence = bool(sight_has_jellyfishes)

        if jellyfishes_presence:
            values = self.jellyfishes_abundance(sight)
        else:
            values = [0 for name in self.jellyfishes_names]

        return values

    def jellyfishes_abundance(self, sight):
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
            value = int(var[1]) if int(var[1]) > 0 else "NA"
            jellyfishes_abundance[key] = value

        values = []
        for jellyfish_name in self.jellyfishes_names:
            try:
                values.append(jellyfishes_abundance[jellyfish_name])
            except KeyError:
                if self.jellyfishes_presence(jellyfish_name, sight):
                    values.append("NA")
                else:
                    values.append(0)
        return values

    def jellyfishes_presence(self, name, sight):
        jellyfishes_presence_vars = sight.sightvariables_set.filter(
            variable__variable__label__contains=name,
            value="1.00",
        )
        jellyfishes_presence_vars = jellyfishes_presence_vars.filter(
            variable__variable__label__contains=self.presence_keyword,
        )
        return bool(jellyfishes_presence_vars)
