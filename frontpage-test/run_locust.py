#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from argparse import Namespace
import logging
import click
from locust import runners
import os, sys

digitransit_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.append(digitransit_path)

from utils.find_limit import find_limit
from utils.plot_median_and_rps import plot_median_and_rps
import locustfile

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option("-h", '--host',
              default='http://dev.digitransit.fi/', show_default=True)
@click.option("-n", '--num_clients',
              default=10, show_default=True)
@click.option("-m", '--median_latency',
              default=300, show_default=True)
@click.option("-r", '--requests_per_client',
              default=10, show_default=True)

def main(num_clients, host, median_latency, requests_per_client):
    results = find_limit(locustfile.FrontpageUser,
                         num_clients,
                         host,
                         median_latency,
                         requests_per_client)

    plot_median_and_rps(results)

if __name__ == '__main__':
    main()
