import random

from locust import HttpLocust, TaskSet, task


class SuggestBehavior(TaskSet):
    min_wait = 100
    max_wait = 500

    @task(2)
    def index(self):
        street = 'Mannerheimintie'
        for i in range(len(street)):
          self.client.get("/autocomplete?text=" + "Mannerheimintie"[0:i],
                          name="suggest")


class TypingUser(HttpLocust):
    task_set = SuggestBehavior
    host = 'http://dev.digitransit.fi/pelias/v1'
