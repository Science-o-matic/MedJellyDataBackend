import csv
from django.core.management.base import BaseCommand
from sights.models import Beach, Variable, MeasureUnit


class Command(BaseCommand):
    args = 'csvfile'
    help = 'Parse csvfile creating beachs'

    def handle(self, *args, **options):
        file = open(args[0])
        csvReader = csv.reader(file)
        for row in csvReader:
            beach = {
                "name": row[0].strip(),
                "code": row[1].strip()
            }
            variable = {
                "type": row[2].strip(),
                "variable_description": row[3].strip(),
                "code": row[4].strip()
            }
            measure_unit = {
                "name": row[5].strip()
            }

            self.create_beach(beach)
            self.create_variable(variable)
            self.create_measure_unit(measure_unit)


    def create_beach(beach):
        Beach.get_or_create(name=beach.name, code=beach.code)

    def create_variable(variable):
        Beach.get_or_create(name=beach.name, code=beach.code)

    def create_variable(measure_unit):
        Beach.get_or_create(name=measure_unit.name)
