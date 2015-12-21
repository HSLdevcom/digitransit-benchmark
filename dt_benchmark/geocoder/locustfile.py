# -*- coding: utf-8 -*-
from random import choice
import codecs

from locust import HttpLocust, TaskSet, task

streets = []
with codecs.open('streetnames.txt', 'r', 'utf-8') as f:
    for line in f.readlines():
        streets.append(line)

class SuggestBehavior(TaskSet):
    min_wait = 100
    max_wait = 500

    @task(2)
    def index(self):
        street = choice(streets)
        for i in range(2, len(street)):
            params = "/autocomplete?text=" + street[0:i]
            self.client.get(params, name="suggest")


class User(HttpLocust):
    task_set = SuggestBehavior
