import os
import csv
import datetime
import paramiko
from django.core.management.base import BaseCommand
from django.conf import settings
from sights.models import Sight, SightVariables, Beach, ReportingClient, BeachVariable
from sights import mailer


class Command(BaseCommand):
    help = 'Pull FTP sights files and import content into sights models'
    reported_from = ReportingClient.objects.get(name="FTP")


    def handle(self, *args, **options):
        self.log("--- Connecting %s" % settings.ACANET_FTP['host'])
        transport = paramiko.Transport((settings.ACANET_FTP['host'],
                                        settings.ACANET_FTP['port']))
        transport.connect(username = settings.ACANET_FTP['user'],
                          password = settings.ACANET_FTP['password'])
        self.sftp = paramiko.SFTPClient.from_transport(transport)
        self.log("Connected")
        self.sftp.chdir(settings.ACANET_FTP['out_path'])
        for f in self.sftp.listdir():
            self.import_sights_file(f)
            self.log("Imported %s" %  f)
        self.sftp.close()
        self.log("--- Disconnected. Import DONE.")

    def log(self, message):
        print datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), message

    def import_sights_file(self, filename):
        sights_file = self.get_sights_file(filename)
        self.log("Parsing and importing...")
        for line in sights_file:
            created = False
            if not line.startswith("*"):
                sight, created = self.create_sight(line)
            if created:
                self.log("Created sight in %s at %s" % (sight, sight.timestamp))
                mailer.notify_new_sight(sight)

    def create_sight(self, line):
        fields = line.split("|")
        timestamp = fields[0].replace("/", "-")
        beach_code = fields[1]
        variable = {
            "code": fields[2],
            "value": fields[3].replace(",", ".")
        }
        beach = Beach.objects.get(code=beach_code)
        sight, created = Sight.objects.get_or_create(timestamp=timestamp,
                                                     beach=beach,
                                                     reported_from=self.reported_from)
        beach_variable = BeachVariable.objects.get(code=variable["code"])
        SightVariables.objects.get_or_create(sight=sight,
                                      variable=beach_variable,
                                      value=variable["value"])
        return (sight, created)



    def get_sights_file(self, filename):
        self.log("GET %s" % filename)
        local_file_path = os.path.join("/tmp/", filename)
        self.sftp.get(filename, local_file_path)
        return open(local_file_path)
