Install with::

    virtualenv testenv
    . testenv/bin/activate
    pip install click matplotlib locustio

Run with::
    . testenv/bin/activate
    ./run_locust.py -n 50 -m 300 -r 500
