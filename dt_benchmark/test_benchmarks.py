# -*- coding: utf-8 -*-
import logging

from dt_benchmark.utils import find_limit


logging.basicConfig(level=logging.DEBUG)


def test_ui():
    from dt_benchmark.ui.locustfile import User as UIUser
    results = find_limit(UIUser,
                         num_clients=1,
                         host='http://dev.digitransit.fi/',
                         median_latency=1,
                         # Locust resets stats after spawning all clients to
                         # prevent low load in the beginning from skewing the
                         # overall stats. So with low client numbers there must
                         # be enough requests to make the test long enough
                         # (there's a race condition between the client finishing
                         # its job before the spawner resets the stats).
                         requests_per_client=10)


def test_otp():
    from dt_benchmark.otp.locustfile import User
    results = find_limit(User,
                         num_clients=1,
                         host='http://dev.digitransit.fi/otp/otp/routers/default/',
                         median_latency=1,
                         requests_per_client=10)


def test_geocoder():
    from dt_benchmark.geocoder.locustfile import User
    results = find_limit(User,
                         num_clients=1,
                         host='http://dev.digitransit.fi/pelias/v1',
                         median_latency=10,
                         requests_per_client=10)
