#!/usr/bin/env python3

"""Intinor Direkt API Python tutorial

Example 1: Send a request to a Direkt unit using the "direkt" module
           and obtain API information as a JSON string
"""

import sys

# The "direkt" module wraps the "requests" library with some convenient
# functionality for the Intinor Direkt API.
import direkt


# START of configuration

# Replace the below example ID "D0****" with the ID of your Direkt unit to
# create the correct Direkt unit URL. This will point to the API root.
# Case-sensitive: Write the Direkt ID with a capital "D".
DIREKT_ID = "D0****"

# Assign "DIREKT_HOST" the hostname or IP address of your Direkt unit or
# "iss.intinor.com" if you want to send requests to the API through ISS.
DIREKT_HOST = "Hostname-or-IP-address"

# Replace username and password in the authentication below with the actual
# username and password for your Direkt unit or for your ISS account, if you
# assigned "DIREKT_HOST" with "iss.intinor.com".
AUTHENTICATION = ("username", "password")

# NOTES:

# Writing credentials into a script is not a secure practise but it makes a
# quick and easy start possible. Choose a more secure approach for usage beyond
# this tutorial.

# The default credentials for your Direkt unit can only be used through local
# network connections and we recommend changing them for security. This can be
# done in the unit's webinterface or in ISS.

# We recommend creating a shared API user account for your team.

# END of configuration


# The URL to the API root is created here. The API root is a good starting
# point resource which is available on all Direkt unit types.
URL = "https://" + DIREKT_HOST + "/api/v1/units/" + DIREKT_ID


def main():
    """Obtain the API resource"""

    # Use a GET request to obtain the API resource.
    response = direkt.get(URL, auth=AUTHENTICATION)

    # Show the text property of the response, which is in JSON string format.
    print(response.text)

    if not response.ok:
        sys.exit("GET '" + URL + "' failed.")


if __name__ == '__main__':
    main()


# We recommend using the "direkt" module for API requests through local network
# connections and through ISS connections but alternatively it is possible to
# access the API without using the "direkt" module, in which case you import
# the "requests" library and connect through ISS.
# See Example 2 for more information.
