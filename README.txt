Install with::

    virtualenv testenv
    # Or `virtualenv --system-site-packages testenv` to avoid compiling lots of C,
    # if `apt-get install python-matplotlib` is run beforehand
    . testenv/bin/activate
    # Only necessary on Python 3, since locustio doesn't officially support 3
    pip install -r requirements.txt
    pip install .

Run with::

    . testenv/bin/activate
    dt_benchmark -n 50 -m 300 -r 500 otp
    
    # Using specified host
    dt_benchmark -n 50 -m 300 -r 500 -h http://api.digitransit.fi/routing/v1/routers/hsl/ otp

Test with::

    pip install --user tox
    tox
