#!/usr/bin/env python3

"""Intinor Direkt API Python tutorial

Example 3: Set video input description
"""

import sys
from datetime import datetime

# The "direkt" module wraps the "requests" library with some convenient
# functionality for the Intinor Direkt API.
import direkt


# START of configuration

# Replace the below example ID "D0****" with the ID of your Direkt unit.
# Case-sensitive: Write the Direkt ID with a capital "D".
DIREKT_ID = "D0****"

# Assign "DIREKT_HOST" the hostname or IP address of your Direkt unit or
# "iss.intinor.com" if you want to send requests to the API through ISS.
DIREKT_HOST = "Hostname-or-IP-address"

# Adjust the value for "VIDEO_INPUT_NUMBER" to the number of the video input
# source for which you wish to set the description.
VIDEO_INPUT_NUMBER = 1

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


# In the API the numbering starts at 0, e.g. "/0/" refers to the first video
# input source. For convenience, in this code "-1" is automatically applied to
# "VIDEO_INPUT_NUMBER" to calculate "VIDEO_INPUT_NUMBER_API".
VIDEO_INPUT_NUMBER_API = str(VIDEO_INPUT_NUMBER - 1)

# The URL for the settings of the chosen video input is created here.
URL = ("https://" + DIREKT_HOST + "/api/v1/units/" + DIREKT_ID +
       "/video_inputs/" + VIDEO_INPUT_NUMBER_API + "/settings")


def main():
    """Set the description for a video input"""

    # Use a GET request to obtain the API resource, in this case the JSON
    # string that stores the settings for the video input source.
    response = direkt.get(URL, auth=AUTHENTICATION)

    if not response.ok:
        print(response.text)
        sys.exit("GET '" + URL + "' failed.")

    # Show how the complete JSON string looks like.
    print("Complete JSON string - before the update:\n\n", response.text)

    # Convert the JSON string into a Python dictionary to access its separate
    # key-value-pairs.
    video_input = response.json()

    # As an example, show how the description in the video input settings looks
    # like, before the update.
    print("\nDescription - before the update:\n" + video_input["description"])

    # Create a timestamp for the description update.
    current_time = datetime.now().strftime("%H:%M:%S")

    # Update the description in the dictionary.
    video_input["description"] = ("SDI in 1 - Last description update at " +
                                  current_time)

    # Use a PUT request to update the video input description on your unit.
    # If the PUT request is successful it returns the updated resource.
    # Through storing this response in a variable an additional GET request
    # can be skipped.
    response = direkt.put(URL, auth=AUTHENTICATION, json=video_input)

    if not response.ok:
        print(response.text)
        sys.exit("PUT '" + URL + "' failed.")

    # Convert the updated JSON string into a Python dictionary as well.
    video_input = response.json()

    # See how the description looks like after the update.
    print("\nDescription - after the update:\n" + video_input["description"])


if __name__ == '__main__':
    main()
