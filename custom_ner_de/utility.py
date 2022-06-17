""" utility.py

Utility class ."""

from __future__ import annotations

import os
from zipfile import ZipFile


class Utility:

    @staticmethod
    def unzip(zip_path: str,
              unzip_path: str,
              verbose: bool = False) -> None:
        """

        :param zip_path: complete path to zip file including filename and extension
        :param unzip_path: complete path to folder
        :param verbose: flag for verbose output, defaults to False
        """

        with ZipFile(file=zip_path, mode="r") as zip_object:
            zip_object.extractall(path=unzip_path)
            if verbose is True:
                print(f"{len(os.listdir(unzip_path))} files unzipped to {unzip_path}.")

    @staticmethod
    def zip_from_memory() -> None:
        """"""

        pass
