"""The "direkt" module provides a best-practice connection mode to your Intinor
Direkt unit's API. The first connection attempt for each request will be done
with the "requests" library requiring a valid certificate. If this does not
succeed the second connection attempt will be done without strict hostname
checking using an Intinor issued HTTPS certificate.

While we recommend using the "direkt" module, alternatives are available. An
alternative is connecting to Direkt units through ISS explicitly using the
"requests" library. If you wish instead to directly connect to your unit
without using the "direkt" module (and not connect through ISS), e.g. under use
of a third-party certificate, please contact Intinor support.

Contact Intinor support for more information on Direkt unit usage and how to
secure your API infrastructure.
"""

import os
import requests


def request(method, url, **kwargs):
    """Sends a request trying default certificate validation and if that does
    not succeed a retry is made with a custom certificate handler that
    validates against a factory default custom Intinor CA signed certificate.
    """

    with requests.Session() as session:
        try:
            # First try with the default HTTPAdapter
            return session.request(method=method, url=url, **kwargs)

        except requests.exceptions.SSLError:
            # Retry using a factory default custom Intinor CA signed
            # certificate.
            session.mount('https://', _DirektCheckingAdapter())
            return session.request(method=method, url=url, **kwargs)


def get(url, params=None, **kwargs):
    """Sends a GET request."""

    return request('get', url, params=params, **kwargs)


def options(url, **kwargs):
    """Sends an OPTIONS request."""

    return request('options', url, **kwargs)


def head(url, **kwargs):
    """Sends a HEAD request."""

    kwargs.setdefault('allow_redirects', False)
    return request('head', url, **kwargs)


def post(url, data=None, json=None, **kwargs):
    """Sends a POST request."""

    return request('post', url, data=data, json=json, **kwargs)


def put(url, data=None, **kwargs):
    """Sends a PUT request."""

    return request('put', url, data=data, **kwargs)


def patch(url, data=None, **kwargs):
    """Sends a PATCH request."""

    return request('patch', url, data=data, **kwargs)


def delete(url, **kwargs):
    """Sends a DELETE request."""

    return request('delete', url, **kwargs)


class _DirektCheckingAdapter(requests.adapters.HTTPAdapter):
    """Custom hostname / CA checking adapter for direct access to a Direkt
    unit's API
    """

    def __init__(self):
        super().__init__()
        this_path = os.path.abspath(__file__)

        # The cacert.pem file is required to be in the same directory as the
        # direkt.py file. It verifies the default certificate that is installed
        # on Direkt units.
        self.intinor_ca = os.path.dirname(this_path) + '/cacert.pem'

    def cert_verify(self, conn, url, verify, cert):
        """If your Direkt unit does not have a valid DNS name or HTTPS
        certificate we offer an alternative certificate validation method using
        an Intinor issued HTTPS certificate without strict hostname checking.
        """

        verify = self.intinor_ca
        conn.assert_hostname = False
        return super().cert_verify(conn, url, verify, cert)
