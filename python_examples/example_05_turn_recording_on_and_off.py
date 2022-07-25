#!/usr/bin/env python3

"""Intinor Direkt API Python tutorial

Example 5: Turn recording on and off

Recording options are available on Direkt Link and Direkt Router. If you are
using Direkt Receiver for this tutorial continue with Example 6.
"""

import sys
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

# Adjust the value for "ENCODER_NUMBER" to the number of the encoder from which
# you wish to record.
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

# The URL for the encoder settings is created here.
ENCODER_SETTINGS_URL = ("https://" + DIREKT_HOST + "/api/v1/units/" + DIREKT_ID
                        + "/encoders/" + ENCODER_NUMBER_API + "/settings")

# The URL for the recording settings is created here.
RECORDING_SETTINGS_URL = ("https://" + DIREKT_HOST + "/api/v1/units/" +
                          DIREKT_ID + "/recording/settings")


def set_recording(recording_value):
    """Help function to start or stop a recording session"""

    response = direkt.get(RECORDING_SETTINGS_URL, auth=AUTHENTICATION)

    if not response.ok:
        print(response.text)
        sys.exit("GET '" + RECORDING_SETTINGS_URL + "' failed.")

    recording = response.json()

    # No need to assign with "recording_value" if it is already correct.
    if recording["active"] == recording_value:
        return response

    recording["active"] = recording_value

    # Strip metadata before reuse. Reduces following request overhead.
    del recording["_links"]

    # Start or stop actual recording session, depending on "recording_value".
    response = direkt.put(RECORDING_SETTINGS_URL, auth=AUTHENTICATION,
                          json=recording)

    if not response.ok:
        print(response.text)
        sys.exit("PUT '" + RECORDING_SETTINGS_URL + "' failed.")

    return response


def main():
    """Turn recording on and off"""

    # Use a GET request to obtain the API resource.
    response = direkt.get(ENCODER_SETTINGS_URL, auth=AUTHENTICATION)

    if not response.ok:
        sys.exit("GET '" + ENCODER_SETTINGS_URL + "' failed.")

    # Show how the complete JSON string looks like.
    print("Complete JSON string for encoder settings:\n\n", response.text)

    # Convert the JSON string into a Python dictionary to access its separate
    # key-value-pairs.
    encoder = response.json()

    # 1) For recording, at least one recording format has to be enabled on your
    # unit. The most commonly enabled recording format is MPEG-TS.
    # 2) Also, the recording format of choice has to be activated in the
    # encoder settings, before the recording can be started. It is possible to
    # activate several recording formats at the same time on one unit. In that
    # case, separate recording files will be stored for all activated recording
    # formats, when a recording session is started.
    # 3) The last step is to actually start (and stop) the recording session.

    # Test if recording formats are enabled.
    if encoder["recording"]:
        print("Enabled recording formats on this unit: " +
              str(encoder["recording"]))
    else:
        sys.exit("No recording formats are enabled on your unit")

    # MPEG-TS is the default recording format in this example.
    if encoder["recording"]["mpegts"]:
        recording_format = "mpegts"

    # If MPEG-TS is not enabled on your unit another format can be chosen from
    # the list of enabled formats.
    else:
        keyboard_input = input("Enter a recording format from the list: ")
        if keyboard_input in encoder["recording"]:
            recording_format = keyboard_input
            print(recording_format + " was chosen as recording format")
        else:
            sys.exit("Input is no enabled recording format")

    # Store the activation status for the chosen recording format as a boolean.
    format_activation = encoder["recording"][recording_format]["active"]

    # Show the activation status for the chosen recording format.
    print("\nRecording format activation status:", format_activation, "\n")

    # If the chosen recording format is not activated, activate it.
    if not format_activation:

        # Update the activation status for the chosen recording format in your
        # dictionary (other formats analogously).
        encoder["recording"][recording_format]["active"] = True

        # Strip metadata before reuse. Reduces following request overhead.
        del encoder["_links"]

        # Use a PUT request to activate the recording format. If the PUT
        # request is successful it returns the updated resource. Through
        # storing this response an additional GET request can be skipped.

        response = direkt.put(ENCODER_SETTINGS_URL,
                              auth=AUTHENTICATION, json=encoder)

        if not response.ok:
            sys.exit("PUT '" + ENCODER_SETTINGS_URL + "' failed.")

        # Convert the updated JSON string into a Python dictionary as well.
        encoder = response.json()

        # See what the recording format activation status after the update is.
        print("Recording format activation status - after the update:",
              encoder["recording"][recording_format]["active"], "\n")

    # Start the recording session.
    response = set_recording(True)

    # Recording is now turned on for the activated format or formats.
    # See what the recording status after starting the recording session is.
    recording = response.json()
    print("Recording status =", recording["active"])

    # After 10 seconds the recording session will be stopped.
    print("Recording turned on for 10 seconds")
    for i in range(10):
        time.sleep(1)
        print(i + 1)

    # Stop the recording session.
    response = set_recording(False)

    # Recording is now turned off again for the activated format or formats.
    # See what the recording status after stopping the recording session is.
    recording = response.json()
    print("Recording status =", recording["active"], "\nRecording turned off")

    # You can also check the recording status through visiting the recording
    # settings URL in your browser.


if __name__ == '__main__':
    main()


# The recording file or files have been stored. If no recording file has been
# stored, check if your hardware configuration allows to store files.
