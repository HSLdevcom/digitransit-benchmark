# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from dt_benchmark.utils import find_limit

# Locust resets stats after spawning all clients to prevent low load in the
# beginning from skewing the overall stats. So with low client numbers there's
# a race condition between the client finishing its job and the spawner
# resetting the stats.
# Monkeypatch locust to prevent this so we can run simple, fast tests on the
# benchmark itself (the tests assert that they have results).
from locust.stats import RequestStats
def noop(*arg, **kwargs):
    print("Stats reset prevented by monkey patch!")
RequestStats.reset_all = noop


logging.basicConfig(level=logging.DEBUG)


def test_ui():
    from dt_benchmark.ui.locustfile import User as UIUser
    results = find_limit(UIUser,
                         num_clients=1,
                         host='http://dev.digitransit.fi/',
                         median_latency=1,
                         requests_per_client=1)


def test_otp():
    from dt_benchmark.otp.locustfile import User
    results = find_limit(User,
                         num_clients=1,
                         host='http://dev.digitransit.fi/otp/otp/routers/default/',
                         median_latency=1,
                         requests_per_client=1)


def test_geocoder():
    from dt_benchmark.geocoder.locustfile import User
    results = find_limit(User,
                         num_clients=1,
                         host='http://dev.digitransit.fi/pelias/v1',
                         median_latency=1,
                         requests_per_client=1)
