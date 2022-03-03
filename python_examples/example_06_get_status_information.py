#!/usr/bin/env python3

"""Intinor Direkt API Python tutorial

Example 6: Build a real-time status feed for the total bitrate and other
           information

This example requires the "curses" library to be installed.
"""

import sys
import curses
import time

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

# Adjust the value for "ENCODER_NUMBER" to the number of the encoder which you
# want to see in the status feed.
ENCODER_NUMBER = 1

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


# In the API the numbering starts at 0, e.g. "/0/" refers to the first encoder.
# For convenience, in this code "-1" is automatically applied to
# "ENCODER_NUMBER" to calculate "ENCODER_NUMBER_API".
ENCODER_NUMBER_API = str(ENCODER_NUMBER - 1)

# The URL for the encoder status is created here.
URL = ("https://" + DIREKT_HOST + "/api/v1/units/" + DIREKT_ID +
       "/encoders/" + ENCODER_NUMBER_API + "/status")


# Define a function which is passed to the curses wrapper.
def encoder_status(stdscr):
    """Show momentary values for a few selected status elements in a feed"""

    curses.curs_set(0)

    # Obtain the momentary status information repeatedly (30 times).
    for _ in range(30):

        # Use a GET request to obtain the API resource.
        response = direkt.get(URL, auth=AUTHENTICATION)

        if not response.ok:
            print(response.text)
            sys.exit("GET '" + URL + "' failed.")

        # Convert the JSON string into a Python dictionary to access its
        # separate key-value-pairs.
        encoder = response.json()

        # Store the momentary values of the status elements that shall be
        # included in the feed.
        description = encoder["description"]
        total_bitrate = encoder["encoding"]["total_bitrate"]

        video_framerate = encoder["encoding"]["video"]["format"]["framerate"]
        width = encoder["encoding"]["video"]["format"]["width"]
        height = encoder["encoding"]["video"]["format"]["height"]
        interlaced = encoder["encoding"]["video"]["format"]["interlaced"]

        audio_sample_rate = (encoder["encoding"]["audio"][0]
                                    ["format"]["sample_rate"])
        number_of_audio_channels = (encoder["encoding"]["audio"][0]
                                           ["format"]["channels"])
        audio_codec_name = (encoder["encoding"]["audio"][0]
                                   ["codec"]["name"])

        # Create headlines in the Curses window.
        # In Curses the y and x coordinates are switched in comparison to most
        # applications.
        stdscr.addstr(1, 1, "Status feed: " + str(description))
        stdscr.addstr(3, 1, "General:")
        stdscr.addstr(5, 1, "Video:")
        stdscr.addstr(13, 1, "Audio:")

        # Create the elements of the status feed in the Curses window.
        stdscr.addstr(3, 14, "Total bitrate: " + str(total_bitrate))
        stdscr.addstr(5, 18, "Framerate: " + str(video_framerate))
        stdscr.addstr(7, 22, "Width: " + str(width))
        stdscr.addstr(9, 21, "Height: " + str(height))
        stdscr.addstr(11, 17, "Interlaced: " + str(interlaced))
        stdscr.addstr(13, 16, "Sample rate: " + str(audio_sample_rate))
        stdscr.addstr(15, 19, "Channels: " + str(number_of_audio_channels))
        stdscr.addstr(17, 17, "Codec name: " + str(audio_codec_name))

        # Reload the Curses window.
        stdscr.refresh()

        # Create a time interval between the status updates (2 seconds).
        time.sleep(2)


def main():
    """Call the Curses wrapper"""

    curses.wrapper(encoder_status)


if __name__ == '__main__':
    main()


# The Curses window will be closed after 30 status updates. It can be regularly
# closed beforehand with ctrl + c. If an error occurs, try expanding the size
# of your terminal before running the code.
