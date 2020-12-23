import random

from django.test import SimpleTestCase
from django.urls import reverse, resolve

from poll.views import home, create, vote, results





class TestUrls(SimpleTestCase):
    def test_home_url_is_resolved(self):
        url = reverse("home")  # Gets the url of the path named home which is set to '' in urlpatterns
        #               |-----------------| - Resolves the url('') and the function that gets called in this case the function in views called home 
        #               |-----------------|    <function home at 0x000001EBE77A6040>
        self.assertEqual(resolve(url).func, home)
        #                                   |--| - The imported function form poll.views home, <function home at 0x000001EBE77A6040>    
    def test_create_url_is_resolved(self):
        url = reverse("create")  
        self.assertEqual(resolve(url).func, create)
    def test_vote_url_is_resolved(self):
        random_poll = random.randint(1,99)
        url = reverse("vote", args=[random_poll])  
        self.assertEqual(resolve(url).func, vote)
    def test_result_url_is_resolved(self):
        random_poll = random.randint(1,99)
        url = reverse("results", args=[random_poll])  
        self.assertEqual(resolve(url).func, results)
