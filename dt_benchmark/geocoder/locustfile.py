# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import codecs
from pkg_resources import resource_stream
from random import choice

from locust import HttpLocust, TaskSet, task

streets = []
with resource_stream(__name__, 'streetnames.txt') as f:
    for line in f.readlines():
        streets.append(line.decode('utf-8'))


class SuggestBehavior(TaskSet):
    min_wait = 100
    max_wait = 500

    @task
    def index(self):
        street = choice(streets)
        for i in range(2, len(street)):
            params = u"/autocomplete?text=" + street[0:i]
            self.client.get(params, name="suggest")


class User(HttpLocust):
    task_set = SuggestBehavior
