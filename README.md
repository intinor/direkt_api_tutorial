# Intinor Direkt API tutorial

This is an introduction to accessing the Intinor Direkt API using Python.
It presents seven good-practice examples for basic usage of the API.


Example 1: Send a request to a Direkt unit using the "direkt" module
           and obtain API information as a JSON string

Example 2: Send a request to a Direkt unit through Intinor Stream Statistics
           (ISS) and obtain API information as a JSON string

Example 3: Set video input description

Example 4: Download a thumbnail image from a video input

Example 5: Turn recording on and off

Example 6: Build a real-time status feed for the total bitrate and other
           information

Example 7: Reboot or shut down your unit


Notes:

The "direkt" module provides a best-practice connection mode to your Intinor
Direkt unit's API. It wraps the "requests" library with some convenient
functionality which includes certificate handling.

The cacert.pem file is required to be in the same directory as the
direkt.py file. It verifies the default certificate that is installed
on Direkt units.


For more information visit:
intinor.com

Send questions to:
support@intinor.se


This tutorial is licensed under MIT.
For further information see the license document.
