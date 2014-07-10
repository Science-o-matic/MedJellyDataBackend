# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

CURRENT_SITE = Site.objects.get(pk=settings.SITE_ID)

IMPORT_REPORT_MAILS = ('marambio@icm.csic.es', 'lopezcastillo89@gmail.com', 'vfuentes@icm.csic.es')

def notify_new_sighting(sight):
    send_mail('[medjellydata] Nuevo avistamiento reportado desde %s' %
              sight.reported_from.name.lower(),
              "Se ha recibido un nuevo avistamiento reportado desde %s.\n\n" %
              sight.reported_from.name.lower() +
              "Puedes consultarlo en http://%s/admin/sights/sight/%s" % (CURRENT_SITE, sight.id),
              'support@science-o-matic.com',
              User.objects.filter(is_staff=True).values_list("email", flat=True),
              fail_silently=False)


def notify_import_report(report):
    subject = '[medjellydata] Informe de avistamientos importados desde Protección Civíl'

    body = """
Se han recibido %(received)s avistamientos, de los cuales se han importado %(imported)s:
- %(having_jellyfishes)s con presencia de medusas
- %(not_having_jellyfishes)s sin presencia de medusas
""" % report

    if report["failed"]:
        body += "\nNo se han podido importar %(failed)s avistamientos." % report
        for beach in report["not_found_beaches"]:
            body += u"\n- Playa %s no tiene correspondencia en el listado de playas" % beach

        send_mail(subject, body, 'support@science-o-matic.com', IMPORT_REPORT_MAILS,
                  fail_silently=False)
