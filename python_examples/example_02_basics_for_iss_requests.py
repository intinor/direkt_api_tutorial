#!/usr/bin/env python3

"""Intinor Direkt API Python tutorial

Example 2: Send a request to a Direkt unit through Intinor Stream Statistics
           (ISS) and obtain API information as a JSON string
"""

import sys
import requests


# The Intinor Direkt API can be accessed through ISS or through a network
# connection to your Direkt unit. This example shows how an API resource can
# be obtained through ISS without using the "direkt" module.


# START of configuration

# Replace the below example ID number "D0****" with the ID of your unit to
# create the correct ISS unit URL. This will point to the API root.
# Case-sensitive: Write the Direkt ID with a capital "D".
DIREKT_ID = "D0****"

# Replace username and password in the authentication below with the actual
# username and password for your ISS account.
AUTHENTICATION = ("username", "password")

# NOTE: Writing credentials into a script is not a secure practise but it makes
# a quick and easy start possible. Choose a more secure approach for usage
# beyond this tutorial.

# END of configuration


# The URL to the API root is created here. The API root is a good starting
# point resource which is available on all Direkt unit types.
URL = "https://iss.intinor.com/api/v1/units/" + DIREKT_ID


def main():
    """Obtain the API resource"""

    # Use a GET request to obtain the API resource.
    response = requests.get(URL, auth=AUTHENTICATION)

    # Show the text property of the response, which is in JSON string format.
    print(response.text)

    if not response.ok:
        sys.exit("GET '" + URL + "' failed.")


if __name__ == '__main__':
    main()


# While API requests through ISS can be done explicitly using the "requests"
# library as shown in this example, we instead recommend using the "direkt"
# module. See Example 1 for more information.
