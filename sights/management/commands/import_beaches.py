import csv
from django.core.management.base import BaseCommand
from sights.models import Beach, Variable, BeachVariable, MeasureUnit


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
                "description": row[3].strip(),
                "code": row[4].strip()
            }
            measure_unit = {
                "name": row[5].strip()
            }

            beach_object = self.create_beach(beach)
            measure_unit_object = self.create_measure_unit(measure_unit)
            self.create_variable(variable, beach_object, measure_unit_object)


    def create_beach(self, beach):
        beach_object, _ = Beach.objects.get_or_create(name=beach["name"], code=beach["code"])
        return beach_object

    def create_variable(self, variable, beach_object, measure_unit_object):
        var, _ = Variable.objects.get_or_create(type=variable["type"],
                                                description=variable["description"],
                                                measure_unit=measure_unit_object)
        BeachVariable.objects.get_or_create(variable=var,
                                            code=variable["code"],
                                            beach=beach_object,)


    def create_measure_unit(self, measure_unit):
        measure_unit_object, _ = MeasureUnit.objects.get_or_create(name=measure_unit["name"])
        return measure_unit_object
