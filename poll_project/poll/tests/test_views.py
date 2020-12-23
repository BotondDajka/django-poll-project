from django.test import TestCase, Client
from django.urls import reverse, resolve
import json

from poll.models import Poll

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse("home")

    def test_poll_home_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "poll/home.html")


    def test_poll_results_GET(self):

        poll = Poll.objects.create()

        url = reverse("results", args=[poll.id])

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "poll/results.html")
