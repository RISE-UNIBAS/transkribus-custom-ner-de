""" client.py

Client class ."""

from __future__ import annotations

import os
from zipfile import ZipFile


class Client:

    @staticmethod
    def unzip(zip_path: str,
              unzip_path: str) -> None:
        """

        :param zip_path: complete path to zip file including filename and extension
        :param unzip_path: complete path to folder
        """

        with ZipFile(file=zip_path, mode="r") as zip_object:
            zip_object.extractall(path=unzip_path)
            print(f"{len(os.listdir(unzip_path))} files unzipped to {unzip_path}.")


