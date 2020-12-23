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