import urllib2, base64
from lxml import etree as ET
from django.conf import settings


class XMLExporter(object):

    def XMLnode(self, name, XMLNodeText=None, **kwargs):
        node = ET.Element(name, kwargs)
        if XMLNodeText:
            node.text = str(XMLNodeText)
        return node


class FTPExporter(XMLExporter):
    filename_template = "ICM_PLAT_%s.dat"

    def __init__(self, instance):
        self.instance = instance

    def export(self):
        from sights.models import SightVariables, VariablesGroup

        root = ET.Element('six')
        code = "ICM%s-%s" % (self.instance.id, self.instance.timestamp.strftime('%Y%m%d'))
        timestamp = self.instance.timestamp.strftime('%d/%m/%Y %H:00')
        sight = ET.Element('mostreig', codi=code, tipus="PLAJ", timestamp=timestamp,
                           observacions="prueba" if settings.DEBUG else "")
        for group in VariablesGroup.objects.all():
            grup = ET.Element('grup', codi=group.name, observacions="")
            for sightvariable in SightVariables.objects.filter(sight=self.instance,
                                                               variable__variable__group=group):
                var = ET.Element('var')
                var_timestamp = ET.Element("timestamp")
                var_timestamp.text = str(timestamp)
                var.append(var_timestamp)
                var_estacio = ET.Element("estacio")
                var_estacio.text = self.instance.beach.code
                var.append(var_estacio)
                var_sightvariable = ET.Element("variable")
                var_sightvariable.text = sightvariable.variable.code
                var.append(var_sightvariable)
                var_profunditat = ET.Element("profunditat")
                var_profunditat.text = "1"
                var.append(var_profunditat)
                var_valor = ET.Element("valor")
                var_valor.text = str(sightvariable.value)
                var.append(var_valor)
                var_motiuInvalid = ET.Element("motiuInvalidacio")
                var_motiuInvalid.text = "0"
                var.append(ET.Element("motiuInvalidacio"))
                var.append(ET.Element("anotacio"))
                var_unitatMesura = ET.Element("unitatMesura")
                var_unitatMesura.text = sightvariable.variable.variable.measure_unit.name
                var.append(var_unitatMesura)
                grup.append(var)
            sight.append(grup)
        root.append(sight)

        filename = self.filename_template % self.instance.timestamp.strftime('%Y%m%d')
        tree = ET.ElementTree(root)
        tree.write(filename, pretty_print=True,
                   xml_declaration=True, encoding="ISO-8859-1")
        f = open(filename, "a")
        f.write("***** FI DE FITXER *****")
        f.close()


class APIExporter(XMLExporter):

    def __init__(self, instance):
        self.instance = instance
        self.enviroment = 'debug' if settings.DEBUG else 'production'
        self.endpoint_url = self._generate_endpoint_url()
        self.auth_header = self._generate_auth()

    def _generate_endpoint_url(self):
        return settings.ACANET_API[self.enviroment]["url"]

    def _generate_auth(self):
        username = settings.ACANET_API[self.enviroment]["user"]
        password = settings.ACANET_API[self.enviroment]["password"]
        return "Basic %s" % base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    def export(self):
        request = urllib2.Request(self.endpoint_url,
                                  headers={"Authorization": self.auth_header},
                                  data=self.generate_xml())
        result = urllib2.urlopen(request)

    def generate_xml(self):
        root = ET.Element('beaches')
        root.append(self.generate_beach_xml())
        tree = ET.ElementTree(root)
        print ET.tostring(tree, pretty_print=True)
        return ET.tostring(tree, pretty_print=True)

    def generate_beach_xml(self):
        timestamp = self.instance.timestamp.strftime("%Y%m%d %H:00")
        beach = self.XMLnode('beach', id=self.instance.beach.code)
        beach.append(self.XMLnode('flagStatusUpdated', timestamp))
        beach.append(self.XMLnode('flagStatus', "GREEN")) # TODO convert variable to generate this
        beach.append(self.XMLnode('flagReason', 1)) # TODO get variable motiu de la bandera
        beach.append(self.XMLnode('jellyFishStatusUpdated', timestamp))
        beach.append(self.XMLnode('jellyFishStatus', "LOW_WARNING")) # TODO figure out this
        jellyFishes = self.XMLnode('jellyFishes')
        self.add_jellyfishes_xml(jellyFishes)
        beach.append(jellyFishes)
        return beach

    def add_jellyfishes_xml(self, node):
        qs = self.instance.sightvariables_set.exclude(variable__variable__api_export_id=None)
        for var in qs[:2]:
            node.append(self.XMLnode("jellyFish", var.variable.variable.api_export_id))
