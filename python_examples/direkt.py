"""The "direkt" module provides a best-practice connection mode to your Intinor
Direkt unit's API. The first connection attempt for each request will be done
with the "requests" library requiring a valid certificate. If this does not
succeed the second attempt uses a trust-on-first-use (TOFU) model: the server's
TLS certificate fingerprint is compared against a local known-hosts store. On
first contact the user is prompted to accept the fingerprint; on subsequent
connections it is verified automatically. If a fingerprint mismatch is detected
the user is prompted to accept the new fingerprint.

While we recommend using the "direkt" module or something similar, alternatives
are available. An alternative is connecting to Direkt units through ISS explicitly
using the "requests" library. If you wish instead to directly connect to your unit
without using the "direkt" module (and not connect through ISS), e.g. under use
of a third-party certificate, please contact Intinor support.

Contact Intinor support for more information on Direkt unit usage and how to
secure your API infrastructure.
"""

import hashlib
import json
import os
import ssl
import requests
from urllib3.poolmanager import PoolManager

# Path to the known-hosts fingerprint store (next to this file).
_KNOWN_HOSTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'known_hosts.json')


def _load_known_hosts():
    """Load the known-hosts fingerprint store from disk."""
    if os.path.isfile(_KNOWN_HOSTS_PATH):
        with open(_KNOWN_HOSTS_PATH, 'r') as f:
            return json.load(f)
    return {}


def _save_known_hosts(known_hosts):
    """Persist the known-hosts fingerprint store to disk."""
    with open(_KNOWN_HOSTS_PATH, 'w') as f:
        json.dump(known_hosts, f, indent=2, sort_keys=True)


def _fingerprint_from_der(der):
    """Return the SHA-256 hex digest of a DER-encoded certificate."""
    return hashlib.sha256(der).hexdigest()


def _verify_tofu_fingerprint(fingerprint, host, port):
    """Check *fingerprint* against the known-hosts store for *host*:*port*.

    * First contact        – prompt the user to accept the fingerprint.
    * Known & matching     – pass silently.
    * Known & mismatched   – prompt the user to accept the new fingerprint.

    Raises ``RuntimeError`` if the user rejects the fingerprint.
    """
    known_hosts = _load_known_hosts()
    key = f"{host}:{port}"

    if key not in known_hosts:
        print(f"\nUnknown host '{host}:{port}'.")
        print(f"  SHA-256 fingerprint: {fingerprint}")
        answer = input("Trust this certificate? [y/N] ").strip().lower()
        if answer != 'y':
            raise RuntimeError(
                f"Certificate for '{host}:{port}' rejected by user.")
        known_hosts[key] = fingerprint
        _save_known_hosts(known_hosts)

    elif known_hosts[key] != fingerprint:
        print(f"\n*** WARNING: Certificate fingerprint for '{host}:{port}' "
              "has CHANGED! ***")
        print(f"  Previously trusted: {known_hosts[key]}")
        print(f"  Current:            {fingerprint}")
        answer = input("Accept the new certificate? [y/N] ").strip().lower()
        if answer != 'y':
            raise RuntimeError(
                f"Certificate change for '{host}:{port}' rejected by user.")
        known_hosts[key] = fingerprint
        _save_known_hosts(known_hosts)


def request(method, url, **kwargs):
    """Sends a request trying default certificate validation and if that does
    not succeed a retry is made using trust-on-first-use fingerprint
    verification.
    """

    with requests.Session() as session:
        try:
            # First try with the default HTTPAdapter
            return session.request(method=method, url=url, **kwargs)

        except requests.exceptions.SSLError:
            # Fallback: TOFU fingerprint verification performed
            # inline by the adapter during the actual TLS handshake.
            session.mount('https://', _TofuAdapter())
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


class _TofuAdapter(requests.adapters.HTTPAdapter):
    """HTTPS adapter that verifies the server certificate fingerprint using
    trust-on-first-use during the actual request connection.
    """

    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        self.poolmanager = PoolManager(*args, ssl_context=ctx, **kwargs)

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):
        # Disable requests-level verification; we verify the fingerprint
        # ourselves after the TLS handshake completes.
        response = super().send(request, stream=stream, timeout=timeout,
                                verify=False, cert=cert, proxies=proxies)

        # Extract the peer certificate from the underlying socket.
        sock = response.raw._connection.sock
        der = sock.getpeercert(binary_form=True)
        fingerprint = _fingerprint_from_der(der)

        from urllib.parse import urlparse
        parsed = urlparse(response.url)
        host = parsed.hostname
        port = parsed.port or 443

        # This will prompt on first use or on change, and raise on rejection.
        _verify_tofu_fingerprint(fingerprint, host, port)

        return response
