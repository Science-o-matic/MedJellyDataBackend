import base64
import os
import requests
import paramiko
import logging
import datetime
from lxml import etree as ET
from django.conf import settings


logger = logging.getLogger(__name__)

class XMLExporter(object):

    def XMLnode(self, name, XMLNodeText=None, **kwargs):
        node = ET.Element(name, **kwargs)
        if XMLNodeText:
            node.text = unicode(XMLNodeText)
        return node


class FTPExporter(XMLExporter):
    filename_template = "ICM_%s_%s-%s.DAT"
    encoding = "ISO-8859-1"

    def __init__(self, queryset):
        self.queryset = queryset

    def export(self):
        from sights.models import ReportingClient

        for reporting_client in ReportingClient.objects.all():
            root = ET.Element('six')
            for sight in self.queryset.filter(reported_from=reporting_client):
                root.append(self.sight_xml(sight))

            date_timestamp = datetime.datetime.now().strftime("%Y%m%d")
            timestamp = datetime.datetime.now().strftime("%H-%M-%S")
            filename = self.filename_template % (reporting_client.code,
                                                 date_timestamp, timestamp)
            tree = ET.ElementTree(root)
            tree.write(filename, pretty_print=True,
                       xml_declaration=True, encoding=self.encoding)
            f = open(filename, "a")
            f.write("***** FI DE FITXER *****")
            f.close()

            if not settings.DEBUG:
                self.send_to_ftp(filename)

        for sight in self.queryset:
            sight.save_ftp_export()

    def sight_xml(self, sight):
        from sights.models import SightVariables, VariablesGroup

        code = "ICM%s-%s" % (sight.id, sight.timestamp.strftime('%Y%m%d'))
        timestamp = sight.timestamp.strftime('%d/%m/%Y %H:%M')
        sight_xml = ET.Element('mostreig', codi=code, tipus="PLAJ", timestamp=timestamp,
                           observacions=sight.comments)
        for group in VariablesGroup.objects.all():
            grup = ET.Element('grup', codi=group.name, observacions="")
            qs = SightVariables.objects.filter(sight=sight,
                                               variable__variable__ftp_exportable=True,
                                               variable__variable__group=group)
            for sightvariable in qs:
                v = self.create_sight_variable(timestamp, sight, sightvariable)
                grup.append(v)
            self.append_default_boolean_variables(grup, timestamp, sight, group, qs)
            sight_xml.append(grup)
        return sight_xml

    def send_to_ftp(self, filename):
        transport = paramiko.Transport((settings.ACANET_FTP['host'],
                                        settings.ACANET_FTP['port']))
        transport.connect(username = settings.ACANET_FTP['user'],
                          password = settings.ACANET_FTP['password'])
        self.sftp = paramiko.SFTPClient.from_transport(transport)
        self.sftp.put(filename, os.path.join(settings.ACANET_FTP['in_path'], filename))

    def create_sight_variable(self, timestamp, sight, sightvariable):
        var = self.XMLnode('var')
        var.append(self.XMLnode("timestamp", str(timestamp)))
        var.append(self.XMLnode("estacio", sight.beach.code))
        var.append(self.XMLnode("variable",  sightvariable.variable.code))
        var.append(self.XMLnode("profunditat", "1"))
        var.append(self.XMLnode("valor", self._cleaned_value(sightvariable)))
        var.append(self.XMLnode("motiuInvalidacio", "0"))
        var.append(self.XMLnode("anotacio"))
        measure_unit = sightvariable.variable.variable.measure_unit.name
        var.append(self.XMLnode("unitatMesura", measure_unit))
        return var


    def append_default_boolean_variables(self, xmlNode, timestamp, sight, group, qs):
        from sights.models import Variable, BeachVariable, SightVariables

        for variable in Variable.objects.filter(field_type='BooleanField',
                                                group=group,
                                                ftp_exportable=True):
            beach_variable = BeachVariable.objects.get(beach=sight.beach,
                                                       variable=variable)
            if not qs.filter(variable=beach_variable).exists():
                sight_variable = SightVariables(sight=sight,
                                                variable=beach_variable,
                                                value=variable.DEFAULT_BOOLEAN_FIELD_VALUE)
                var = self.create_sight_variable(timestamp, sight, sight_variable)
                xmlNode.append(var)


    def _cleaned_value(self, sightvariable):
        cleaned_value = sightvariable.value
        field_type = sightvariable.variable.variable.field_type
        if field_type == "ChoiceField":
            cleaned_value = int(cleaned_value)
        elif field_type == "DecimalField":
            cleaned_value = str(cleaned_value)
        elif field_type == "BooleanField":
            cleaned_value = int(cleaned_value)
        return str(cleaned_value)


class APIExporter(XMLExporter):
    FLAG_STATUS = ("NO_INFO", "GREEN", "YELLOW", "RED")

    def __init__(self, instance):
        self.instance = instance
        self.enviroment = 'debug' if settings.DEBUG else 'production'
        self.endpoint_url = os.path.join(
            settings.MEDJELLY_API[self.enviroment]["url"],
            'bulkupdate'
        )
        self.auth_header = self._auth_string()

    def _auth_string(self):
        username = settings.MEDJELLY_API[self.enviroment]["user"]
        password = settings.MEDJELLY_API[self.enviroment]["password"]
        return "Basic %s" % base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    def export(self):
        headers = {
            "Content-type": "application/xml",
            "Authorization": self.auth_header
        }
        xml = self.generate_xml()

        logger.info("REQUEST:")
        logger.info(self.endpoint_url)
        logger.info(headers)
        logger.info(xml)

        r = requests.post(self.endpoint_url, data=xml, headers=headers)

        logger.info("RESPONSE:")
        logger.info(r.content)

    def generate_xml(self):
        root = ET.Element('beaches')
        root.append(self.generate_beach_xml())
        tree = ET.ElementTree(root)
        return ET.tostring(tree)

    def generate_beach_xml(self):
        timestamp = self.instance.timestamp.strftime("%Y%m%d %H:%M")

        beach = ET.Element('beach', id=unicode(self.instance.beach.medjelly_api_id))
        beach.append(self.XMLnode('flagStatusUpdated', timestamp))

        flag = self.instance.get_flag()
        beach.append(self.XMLnode('flagStatus', self.FLAG_STATUS[int(flag)]))

        flagReason = self.instance.get_flag_reason()
        beach.append(self.XMLnode('flagReason', str(flagReason)))

        beach.append(self.XMLnode('waterTemperature', str(self.instance.get_water_temp())))

        beach.append(self.XMLnode('jellyFishStatusUpdated', timestamp))
        jellyFishStatus = self.instance.get_jellyFishStatus()
        beach.append(self.XMLnode('jellyFishStatus', jellyFishStatus))

        beach.append(self.jellyfishes_xml())
        return beach

    def jellyfishes_xml(self):
        jellyfishes = self.XMLnode('jellyFishes')
        for j in self.instance.jellyfishes.all():
            jelly = ET.Element('jellyFish',
                               id=unicode(j.jellyfish.medjelly_api_id),
                               abundance=unicode(j.abundance.id),
                               size=unicode(j.size.id),
            )
            jellyfishes.append(jelly)
        return jellyfishes
