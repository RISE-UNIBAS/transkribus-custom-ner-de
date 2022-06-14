""" main.py

Main app. """

from __future__ import annotations
import os.path

DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))

from client import Client

exit()
Client.unzip(PARENT_DIR + "/sample/Protokoll-Zionistenkongress-Basel_1897-0200.zip",
             PARENT_DIR + "/tests")