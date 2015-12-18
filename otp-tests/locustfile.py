from random import choice
from locust import HttpLocust, TaskSet, task
import simplejson

url_params_json = simplejson.load(open("url_params.json"))
set_of_url_params = url_params_json["url_params"]

class OTPBehavior(TaskSet):
    min_wait = 100
    max_wait = 500

    @task(2)
    def index(self):
        url_params = choice(set_of_url_params)
        self.client.get(url_params, name="otp")


class RouteSearchingUser(HttpLocust):
    task_set = OTPBehavior
    host = 'http://dev.digitransit.fi/otp/otp/routers/default/'
