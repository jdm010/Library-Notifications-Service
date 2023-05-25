"""Module to retreive/declare the environment variables."""


import os

LIBRARY_CATALOGUE_SERVER = os.environ.get("LIBRARY_CATALOUGE_SERVER", "")
LIBRARY_CATALOGUE_SERVER_SUFFIX = os.environ.get("LIBRARY_CATALOUGE_SERVER_SUFFIX", "")
