import datetime
import responses
import urllib
import simplejson as json
from urlparse import urljoin
from datetime import datetime
from django.test import TestCase
from django.conf import settings
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from sights.models import Sight, Beach, BeachOwner, City, ReportingClient, Jellyfish, \
    JellyfishSize, JellyfishAbundance
from sights.management.commands.import_proteccion_civil import API_COLUMNS


class TestSightingsExporter(TestCase):
    base_api_url = settings.MEDJELLY_API["production"]["url"]

    def setUp(self):
        city = City.objects.create(name="test city")

        beach_owner = BeachOwner.objects.create(name="test beach owner")

        beach = Beach.objects.create(
            name="test beach",
            city=city,
            owner=beach_owner,
            medjelly_api_id=99999
        )

        self.sighting = Sight.objects.create(
            timestamp=datetime.today(),
            beach=beach,
            reported_from=ReportingClient.objects.all()[0]
        )

    @responses.activate
    def test_export_sighting(self):
        """
        A validated sighting should be marked as sent via API if has been exported
        with a successful response from MedJellyAPI
        """
        responses.add(responses.POST, urljoin(self.base_api_url, "bulkupdate"),
                      body={"status":"OK","info":"Se actualizaron 1 playas"})

        self.sighting.validated = True
        self.sighting.export()

        self.assertEquals(self.sighting.api_sent, True)


class TestSightingsViews(TestCase):
    base_api_url = settings.MEDJELLY_API["production"]["url"]
    date_format = "%d-%m-%Y %H:%M"


    def setUp(self):
        city = City.objects.create(name="test city")
        beach_owner = BeachOwner.objects.create(name="test beach owner")
        self.beach = Beach.objects.create(
            name="test beach",
            city=city,
            owner=beach_owner,
            medjelly_api_id=99999
        )

        self.user = User.objects.create(username="test")
        self.user_password = "test"
        self.user.set_password(self.user_password)
        self.user.save()

        self.jellyfish_size = JellyfishSize.objects.create(id=1, name="size")
        self.jellyfish_abundance = JellyfishAbundance.objects.create(id=1, name="abundance")
        self.jellyfish = Jellyfish.objects.create(name="jelly")

    def _get_new_sighting_url(self):
        response = self.client.post(reverse('api_token_new'), {
            'username': self.user.username,
            'password': self.user_password,
        })

        data = json.loads(response.content)
        return reverse("new_sighting") + "?" + urllib.urlencode(data)

    @responses.activate
    def test_new_sighting_with_no_jellyfishes(self):
        """
        New sighting with no jellyfishes should be correctly created and exported
        automatically to MedJelly API
        """
        responses.add(responses.POST, urljoin(self.base_api_url, "bulkupdate"),
                      body={"status":"OK","info":"Se actualizaron 1 playas"})

        url = self._get_new_sighting_url()
        timestamp = datetime.today().strftime(self.date_format)

        r = self.client.post(url, {
                "timestamp": timestamp,
                "beach": self.beach.id
                })
        self.assertEquals(r.status_code, 200)

        self.assertEquals(Sight.objects.all().count(), 1)
        created_sighting = Sight.objects.all()[0]
        self.assertEquals(created_sighting.beach, self.beach)
        self.assertTrue(created_sighting.timestamp.strftime(self.date_format), timestamp)
        self.assertTrue(created_sighting.api_sent)


    @responses.activate
    def test_new_sighting_with_jellyfishes(self):
        """
        New sighting with jellyfishes should be correctly created and shouldn't be exported
        automatically to MedJelly API
        """
        url = self._get_new_sighting_url()

        r = self.client.post(url, {
                "timestamp": datetime.today().strftime(self.date_format),
                "beach": self.beach.id,
                "jellyfishes": self.jellyfish.id,
                "jellyfishes_sizes": self.jellyfish_size.id,
                "jellyfishes_abundances": self.jellyfish_abundance.id
                })
        self.assertEquals(r.status_code, 200)

        self.assertEquals(Sight.objects.all().count(), 1)
        created_sighting = Sight.objects.all()[0]
        self.assertEquals(created_sighting.jellyfishes.all()[0].jellyfish, self.jellyfish)
        self.assertFalse(created_sighting.api_sent)
