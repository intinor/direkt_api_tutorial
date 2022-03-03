#!/usr/bin/env python3

"""Intinor Direkt API Python tutorial

Example 7: Reboot or shut down your unit
"""

import sys

# The "direkt" module wraps the "requests" library with some convenient
# functionality for the Direkt API.
import direkt


# START of configuration

# Replace the below example ID "D0****" with the ID of your Direkt unit.
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


# The URL for the unit reboot is created here. Instead of "/reboot" you can try
# other available system actions like "/shutdown" as well.
URL = ("https://" + DIREKT_HOST + "/api/v1/units/" + DIREKT_ID +
       "/system/actions/reboot")


def main():
    """Reboot a Direkt unit"""

    # Confirm the reboot through keyboard input.
    keyboard_input = input('Do you want to reboot your unit? "yes" or "no": ')
    if keyboard_input == "yes":
        # Use a POST request to reboot your unit.
        # If the POST request is successful it returns the updated resource.
        # Through storing this response in a variable an additional GET request
        # can be skipped.
        response = direkt.post(URL, auth=AUTHENTICATION)

        if not response.ok:
            print(response.text)
            sys.exit("POST '" + URL + "' failed.")

        # Print the reboot confirmation message from the response.
        print(response.json()["message"])
    else:
        print("Reboot not confirmed")


if __name__ == '__main__':
    main()
