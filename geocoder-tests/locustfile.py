from random import choice

from locust import HttpLocust, TaskSet, task

streets = []
with open('streetnames.txt', 'r') as f:
    for line in f.readlines():
        streets.append(line)

class SuggestBehavior(TaskSet):
    min_wait = 100
    max_wait = 500

    @task(2)
    def index(self):
        street = choice(streets)
        for i in range(2, len(street)):
          self.client.get("/autocomplete?text=" + "Mannerheimintie"[0:i],
                          name="suggest")


class TypingUser(HttpLocust):
    task_set = SuggestBehavior
    host = 'http://dev.digitransit.fi/pelias/v1'
