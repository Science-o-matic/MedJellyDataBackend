from datetime import datetime
from django.test import TestCase
from sights.models import Sight, Beach, BeachOwner, City, ReportingClient


class TestSightingsExporter(TestCase):

    def setUp(self):
        city = City.objects.create(name="test city")
        beach_owner = BeachOwner.objects.create(name="test beach owner")
        beach = Beach.objects.create(
            name="test beach",
            city=city,
            owner=beach_owner,
            medjelly_api_id=1
        )

        self.sighting = Sight.objects.create(
            timestamp=datetime.today(),
            beach=beach,
            reported_from=ReportingClient.objects.all()[0]
        )

    def test_export_sight(self):
        self.sighting.validated = True
        self.sighting.export()
        self.assertEquals(self.sighting.api_sent, False)
