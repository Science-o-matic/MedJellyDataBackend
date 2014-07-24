# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

CURRENT_SITE = Site.objects.get(pk=settings.SITE_ID)

IMPORT_REPORT_MAILS = ('marambio@icm.csic.es', 'lopezcastillo89@gmail.com', 'vfuentes@icm.csic.es',
                       'antonio.barcia@gmail.com', 'maca.jellyrisk@gmail.com',
                       )

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

    report["admin_url"] = ""
    if report["sightings_having_jellyfishes"]:
        report["admin_url"] = "http://%s/admin/sights/sight/?id__in=%s" % (
            CURRENT_SITE, ",".join([str(s.id) for s in report["sightings_having_jellyfishes"]])
         )

    body = "Se han recibido %(received)s avistamiento/s, " % report
    body += "de los cuales se han importado %(imported)s." % report
    if report["imported"]:
        body += "\n- %(having_jellyfishes)s con presencia de medusas. %(admin_url)s" % report
        body += "\n- %(not_having_jellyfishes)s sin presencia de medusas." % report

    if report["sightings_auto_exported"]:
        n = len(report["sightings_auto_exported"])
        body += "\n\nSe han exportado %s avistamiento/s automáticamente:" % n
        for sighting in report["sightings_auto_exported"]:
            body += "\n- Avistamiento %s" % sighting


    if report["failed"]:
        body += "\n\nNo se han importado %(failed)s avistamiento/s:" % report
        for beach in report["not_found_beaches"]:
            body += u"\n- Playa %s no tiene correspondencia en el listado de playas" % beach
        for sighting in report["sightings_already_imported"]:
            body += "\n- Avistamiento %s ya había sido importado previamente." % sighting

    send_mail(subject, body, 'support@science-o-matic.com', IMPORT_REPORT_MAILS,
              fail_silently=False)
