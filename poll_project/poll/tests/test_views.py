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


    def test_poll_non_existant_result_GET(self):
        url = reverse("results", args=[1])

        response = self.client.get(url)

        self.assertRedirects(response, self.home_url, status_code=302)


    def test_poll_vote_GET(self):

        poll = Poll.objects.create()

        url = reverse("vote", args=[poll.id])

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "poll/vote.html")


    def test_poll_non_existant_vote_GET(self):
        url = reverse("vote", args=[1])

        response = self.client.get(url)

        self.assertRedirects(response, self.home_url, status_code=302)

    def test_poll_create_POST(self):
        url = reverse("create")

        input_data = {
            "question": "the question",
            "option_one": "o1",
            "option_two": "o2",            
            "option_three": "03",
        }
        response = self.client.post(url, data=input_data)

        self.assertRedirects(response, self.home_url, status_code=302)
        actual_value = Poll.objects.values(*input_data.keys())
        expected_value = [input_data]
        self.assertCountEqual(actual_value, expected_value)
