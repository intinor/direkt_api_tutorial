#!/usr/bin/env python3

"""Intinor Direkt API Python tutorial

Example 4: Download a thumbnail image from a video input
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

# Adjust the value for "VIDEO_INPUT_NUMBER" to the number of the video input
# source for which you wish to store a thumbnail image.
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

# The URL for obtaining the thumbnail image is created here. The thumbnail
# image size can be adjusted through setting the width parameter at the end of
# the URL. Aspect ratio will be kept.
URL = ("https://" + DIREKT_HOST + "/api/v1/units/" + DIREKT_ID +
       "/video_inputs/" + VIDEO_INPUT_NUMBER_API + "/thumbnails/0?width=1280")


def main():
    """Download a thumbnail from a video input"""

    # Use a GET request to obtain the thumbnail image.
    response = direkt.get(URL, auth=AUTHENTICATION)

    if not response.ok:
        print(response.text)
        sys.exit("GET '" + URL + "' failed.")

    # Create a file to store the thumbnail. Choose the binary writing mode.
    with open("./thumbnail.png", "wb") as thumbnail_file:
        # Write the binary data into the PNG file.
        # Choose "content" instead of the previously used "text".
        thumbnail_file.write(response.content)

    print("Use an image viewer to see 'thumbnail.png'")


if __name__ == '__main__':
    main()
