Install with::

    virtualenv [--system-site-packages] testenv
    . testenv/bin/activate
    pip install .

Run with::
    . testenv/bin/activate
    dt-benchmark -n 50 -m 300 -r 500 otp
