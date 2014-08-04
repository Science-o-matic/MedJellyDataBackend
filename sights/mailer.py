# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

CURRENT_SITE = Site.objects.get(pk=settings.SITE_ID)

NOTIFY_EMAILS = ('marambio@icm.csic.es', 'lopezcastillo89@gmail.com',
                 'veronica.jellyrisk@gmail.com', 'antonio.barcia@gmail.com',
                 'maca.jellyrisk@gmail.com', 'fuentesmartin@gmail.com'
                 )

def notify_new_sighting(sighting):
    reporting_client = sighting.reported_from.name.lower()

    subject = '[medjellydata] Nuevo avistamiento reportado desde %s' % reporting_client

    body = u"Se ha recibido un nuevo avistamiento reportado desde %s." % reporting_client


    if sighting.api_sent:
        body += u"\nEl avistamiento ha sido exportado automáticamente."

    if sighting.jellyfishes_presence:
        body += u"\nEl avistamiento reporta presencia de medusas."

    body += u"\nPuedes consultarlo en http://%s/admin/sights/sight/%s" % (CURRENT_SITE, sighting.id)

    send_mail(subject, body, 'support@science-o-matic.com', NOTIFY_EMAILS,
              fail_silently=False)


def notify_report(report):
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
            body += u"\n- Avistamiento %s".encode("utf-8") % sighting

    if report["failed"]:
        body += "\n\nNo se han importado %(failed)s avistamiento/s:" % report
        for beach in report["not_found_beaches"]:
            body += u"\n- Playa %s no tiene correspondencia en el listado de playas".encode("utf-8") % beach
        for sighting in report["sightings_already_imported"]:
            body += u"\n- Avistamiento %s ya había sido importado previamente.".encode("utf-8") % sighting

    send_mail(subject, body, 'support@science-o-matic.com', NOTIFY_EMAILS,
              fail_silently=False)
