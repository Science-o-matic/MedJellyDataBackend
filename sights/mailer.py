# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site


def notify_new_sight(sight):
    site = Site.objects.get(pk=settings.SITE_ID)
    send_mail('[medjellydata] Nuevo avistamiento reportado desde %s' % sight.reported_from.name.lower(),
              "Se ha recibido un nuevo avistamiento reportado desde %s.\n\n" % sight.reported_from.name.lower() +
              "Puedes consultarlo en http://%s/admin/sights/sight/%s" % (site, sight.id),
              'support@science-o-matic.com',
              User.objects.filter(is_staff=True).values_list("email", flat=True),
              fail_silently=False)
