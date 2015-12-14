#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from argparse import Namespace
import logging

import click
from locust import runners

import locustfile


def find_limit(num_clients=10,
               host='http://localhost:8888',
               median_latency=300,
               requests_per_client=10
               ):
    options = Namespace()
    options.host = host

    logging.basicConfig(level=logging.INFO)

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
            [locustfile.RouteSearchingUser], options)
        runners.locust_runner.start_hatching(wait=True)
        runners.locust_runner.greenlet.join()

        logging.info('name',
                     'min_response_time',
                     'median_response_time',
                     'max_response_time',
                     'total_rps')
        if runners.locust_runner.errors:
            logging.warn("Got %s errors", len(runners.locust_runner.errors))
            logging.warn(runners.locust_runner.errors.values()[0].error)

        # XXX Handles only locust runner
        value = runners.locust_runner.stats.entries.values()[0]
        assert(len(runners.locust_runner.stats.entries.values()) == 1)
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
        logging.info(value.min_response_time,
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


@click.command()
@click.option("-h", '--host',
              default='http://dev.digitransit.fi/otp/otp/routers/default/', show_default=True)
@click.option("-n", '--num_clients',
              default=10, show_default=True)
@click.option("-m", '--median_latency',
              default=300, show_default=True)
@click.option("-r", '--requests_per_client',
              default=10, show_default=True)
def main(num_clients, host, median_latency, requests_per_client):
    results = find_limit(num_clients,
                         host,
                         median_latency,
                         requests_per_client)
    import matplotlib.pyplot as plt

    ordered_results = sorted(results.items())
    x = [i[0] for i in ordered_results]
    ys = [i[1] for i in ordered_results]
    fig, ax1 = plt.subplots()
    median, = ax1.plot(x, [y[2] for y in ys], label='median', color='b')
    ax1.fill_between(x,
                     [y[1] for y in ys],
                     [y[3] for y in ys],
                    alpha=0.3)
    ax1.set_xlabel('# of concurrent clients')
    ax1.set_ylabel('ms', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    ax2 = ax1.twinx()
    rps, = ax2.plot(x, [y[5] for y in ys], label='rps', color='r')
    ax2.set_ylabel('rps', color='r')
    for tl in ax2.get_yticklabels():
            tl.set_color('r')
    ax2.legend(handles=[median, rps])
    plt.show()


if __name__ == '__main__':
    main()
