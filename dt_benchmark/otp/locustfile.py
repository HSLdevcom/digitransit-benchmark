from __future__ import absolute_import, division, print_function, unicode_literals

from pkg_resources import resource_stream
from random import choice

from locust import HttpLocust, TaskSet, task
import simplejson

set_of_url_params = simplejson.load(
    resource_stream(__name__, 'url_params.json'))["url_params"]


class OTPBehavior(TaskSet):
    min_wait = 100
    max_wait = 500

    @task
    def index(self):
        url_params = choice(set_of_url_params)
        self.client.get(url_params, name="otp")


class User(HttpLocust):
    task_set = OTPBehavior
