#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from argparse import Namespace
import logging
from locust import runners


def find_limit(locustUser,
               num_clients=10,
               host='http://localhost:8888',
               median_latency=300,
               requests_per_client=10):
    options = Namespace()
    options.host = host
    options.num_clients = num_clients
    max = None
    min = 0
    results = {}
    done = False
    while True:
        logging.info('Min, max, current: %s, %s, %s', min, max, options.num_clients)
        options.num_requests = options.num_clients * requests_per_client
        options.hatch_rate = options.num_clients

        # XXX Handles only locust runner
        runners.locust_runner = runners.LocalLocustRunner(
            [locustUser], options)
        runners.locust_runner.start_hatching(wait=True)
        runners.locust_runner.greenlet.join()

        if runners.locust_runner.errors:
            logging.warn("Got %s errors", len(runners.locust_runner.errors))
            logging.warn(runners.locust_runner.errors.values()[0].error)

        # XXX Handles only locust runner
        value = runners.locust_runner.stats.entries.values()[0]
        if value.min_response_time == None:
            logging.error("min_response_time was None, exiting")
            import sys
            sys.exit(-1)

        results[options.num_clients] = (
            value.min_response_time,
            value.get_response_time_percentile(0.05),
            value.median_response_time,
            value.get_response_time_percentile(0.95),
            value.max_response_time,
            value.total_rps)
        logging.info('min_response_time %s, median_response_time %s, max_response_time %s, total_rps %s',
                     value.min_response_time,
                     value.median_response_time,
                     value.max_response_time,
                     value.total_rps)
        if value.median_response_time > median_latency:
            done = True
        if done:
            max = options.num_clients
        else:
            min = options.num_clients
        if max is not None:
            if max < min + 5:
                logging.info("Stopping iteration at %s clients",
                             options.num_clients)
                return results
            options.num_clients = (max + min) / 2
        else:
            options.num_clients = options.num_clients * 2
        done = False
