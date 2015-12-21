#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import logging

import click
from locust import runners

from utils.find_limit import find_limit
from utils.plot_median_and_rps import plot_median_and_rps

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option("-h", '--host')
@click.option("-n", '--num_clients',
              default=10, show_default=True)
@click.option("-m", '--median_latency',
              default=300, show_default=True)
@click.option("-r", '--requests_per_client',
              default=10, show_default=True)
@click.argument('target', type=click.Choice(['geocoder', 'otp', 'ui']))
def main(num_clients, host, median_latency, requests_per_client, target):
    if target == 'geocoder':
        from geocoder.locustfile import User
        if not host:
            host = 'http://dev.digitransit.fi/pelias/v1'
    elif target == 'otp':
        from otp.locustfile import User
        if not host:
            host = 'http://dev.digitransit.fi/otp/otp/routers/default/'
    elif target == 'ui':
        from ui.locustfile import User
        if not host:
            host = 'http://dev.digitransit.fi/'

    results = find_limit(User,
                         num_clients,
                         host,
                         median_latency,
                         requests_per_client)

    plot_median_and_rps(results)

if __name__ == '__main__':
    main()
